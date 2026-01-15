from flask import Flask, request, jsonify, render_template
from models import Task, SessionLocal, engine, Base

Base.metadata.create_all(engine)
app = Flask(__name__, template_folder="../templates")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def list_tasks():
    session = SessionLocal()
    tasks = session.query(Task).all()
    result = [
            {
                'id':           t.id,
                'title':        t.title,
                'description':  t.description,
                'status':       t.status,
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
    task = Task(title=title, description=data.get('description'))
    session.add(task)
    session.commit()
    session.refresh(task)
    session.close()
    return jsonify({'id': task.id}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json() or {}
    session = SessionLocal()
    task = session.query(Task).get(task_id)
    if not task:
        session.close()
        return jsonify({'error': 'not found'}), 404
    task.title =        data.get('title',        task.title)
    task.description =  data.get('description',  task.description)
    task.status =       data.get('status',       task.status)
    session.commit()
    session.close()
    return jsonify({'message': 'updated'}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    session = SessionLocal()
    task = session.query(Task).get(task_id)
    if not task:
        session.close()
        return jsonify({'error': 'not found'}), 404
    session.delete(task)
    session.commit()
    session.close()
    return jsonify({'message': 'deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
