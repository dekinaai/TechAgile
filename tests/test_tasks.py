import json
import os
import tempfile
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from src.app import app
from src.models import Base, engine

# --------------------------------------------------
# Setup / Teardown
# --------------------------------------------------

@pytest.fixture(autouse=True)
def setup_database():
    """
    Cria um banco limpo antes de cada teste.
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def client():
    return app.test_client()


# --------------------------------------------------
# Testes de Criação
# --------------------------------------------------

def test_create_task_success(client):
    response = client.post(
        "/tasks",
        json={"title": "Tarefa Teste", "description": "Descrição"}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data


def test_create_task_with_priority(client):
    response = client.post(
        "/tasks",
        json={"title": "Alta prioridade", "priority": 1}
    )

    assert response.status_code == 201
    task_id = response.get_json()["id"]

    list_response = client.get("/tasks")
    tasks = list_response.get_json()

    assert tasks[0]["priority"] == 1


def test_create_task_without_title(client):
    response = client.post(
        "/tasks",
        json={"description": "Sem título"}
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


# --------------------------------------------------
# Testes de Listagem
# --------------------------------------------------

def test_list_tasks_empty(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.get_json() == []


def test_list_tasks_with_data(client):
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})

    response = client.get("/tasks")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


# --------------------------------------------------
# Testes de Atualização
# --------------------------------------------------

def test_update_task_success(client):
    create_resp = client.post("/tasks", json={"title": "Original"})
    task_id = create_resp.get_json()["id"]

    update_resp = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Atualizado",
            "status": "done",
            "priority": 2
        }
    )

    assert update_resp.status_code == 200

    list_resp = client.get("/tasks")
    task = list_resp.get_json()[0]

    assert task["title"] == "Atualizado"
    assert task["status"] == "done"
    assert task["priority"] == 2


def test_update_nonexistent_task(client):
    response = client.put(
        "/tasks/999",
        json={"title": "Inexistente"}
    )

    assert response.status_code == 404
    assert "error" in response.get_json()


# --------------------------------------------------
# Testes de Remoção
# --------------------------------------------------

def test_delete_task_success(client):
    create_resp = client.post("/tasks", json={"title": "Para remover"})
    task_id = create_resp.get_json()["id"]

    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200

    list_resp = client.get("/tasks")
    assert list_resp.get_json() == []


def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert "error" in response.get_json()


# --------------------------------------------------
# Testes de Regressão / Contrato da API
# --------------------------------------------------

def test_task_fields_contract(client):
    client.post(
        "/tasks",
        json={
            "title": "Contrato",
            "description": "Verificar campos",
            "priority": 3
        }
    )

    response = client.get("/tasks")
    task = response.get_json()[0]

    expected_keys = {
        "id",
        "title",
        "description",
        "status",
        "priority",
        "created_at"
    }

    assert expected_keys.issubset(task.keys())

