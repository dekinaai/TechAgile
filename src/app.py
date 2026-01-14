from flask import Flask, request, jsonify
from models import Task, SessionLocal, engine, Base

Base.metadata.create_all(engine)
app = Flask(__name__)

@app.route('/tasks', methogs=['GET'])
def list_tasks():
    session = SessionLocal()
    tasks = session.query(Task).all()
    result = [
            {
                'id':           t.id,
                'title':        t.title,
                'description':  t.description,
                'status':       t.status,
                'priority':     t.priority,
                'created_at':   t.created_at.isoformat()
            } for t in tasks
             ]
    session.close()
    return jsonify(result), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        return jsonify({'error': 'title required'}), 400
    session = SessionLocal()
    task = Task(title=title, description=data.get('description'), priority=data.get('priority', 3))
    session.add(task)
    session.commit()
    session.refresh(task)
    session.close()
    return jsonify({'id': task.id}), 201

# TODO: PUT e DELETE

if __name__ == '__main__':
    app.run(debug=True)
