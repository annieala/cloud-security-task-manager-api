from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage for tasks
tasks = []
next_id = 1

@app.route('/')
def home():
    return jsonify({
        "message": "Task Manager API",
        "endpoints": {
            "POST /tasks": "Create a new task",
            "GET /tasks": "Retrieve all tasks",
            "DELETE /tasks/<id>": "Delete a task by ID"
        }
    })

@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    task = {
        "id": next_id,
        "title": data['title'],
        "completed": data.get('completed', False)
    }
    
    tasks.append(task)
    next_id += 1
    
    return jsonify({
        "message": "Task created successfully",
        "task": task
    }), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        "total_tasks": len(tasks),
        "tasks": tasks
    }), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if task is None:
        return jsonify({"error": f"Task with id {task_id} not found"}), 404
    
    tasks = [t for t in tasks if t['id'] != task_id]
    
    return jsonify({
        "message": f"Task {task_id} deleted successfully",
        "deleted_task": task
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)