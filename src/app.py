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

# TODO: POST, PUT e DELETE

if __name__ == '__main__':
    app.run(debug=True)
