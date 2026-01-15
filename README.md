# TechAgile

Projeto acadêmico: sistema de gerenciamento de tarefas desenvolvido como atividade da disciplina de Engenharia de Software.

Objetivo: Implementar um pequeno sistema CRUD e demonstrar práticas de projeto ágil, controle de qualidade com GitHub Actions e gestão de mudanças.

## Como executar (local):
```
git clone https://github.com/dekinaai/TechAgile.git
cd TechAgile
source .venv/bin/activate # Linux/Mac
.\.venv\Scripts\activate # Windows
pip install -r requirements.txt
export FLASK_APP=src/app.py
flask run
```

## Testar: 
```
pytest -q
```

**Workflow CI** (GitHub Actions): O workflow executa: instalação de dependências e execução de testes com pytest.

## Mudança de escopo

**Alteração**: Adicionar campo priority às tarefas.

**Justificativa**: O cliente necessita priorizar entregas e distinguir tarefas críticas de tarefas rotineiras em sua operação logística.

**Impacto**: Alteração no modelo de dados, atualizações nas APIs e UI, necessidade de atualização de testes e documentação.

Ações executadas:

- Atualização do modelo Task (+priority).
- Inclusão de testes cobrindo priority.
