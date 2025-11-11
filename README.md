# Task Manager API - Cloud Security

A simple RESTful API built with Flask for managing to-do tasks with CRUD operations, containerized using Docker.

## Quick Start

### Build Docker Image
```bash
docker build -t task-manager-api .
```

### Run Docker Container
```bash
docker run -d -p 5000:5000 --name task-manager task-manager-api
```

### Test API

**Create Task:**
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete lab", "completed": false}'
```

**Get All Tasks:**
```bash
curl http://localhost:5000/tasks
```

**Delete Task:**
```bash
curl -X DELETE http://localhost:5000/tasks/1
```

**Ensuring Security and Compliance in Cloud Software Development (Microsoft Azure)**
