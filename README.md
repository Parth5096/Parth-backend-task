# Task Manager API (Flask)

A RESTful API for managing tasks, built with **Flask**.  
It supports JWT-based authentication, user roles (admin & user), CRUD operations on tasks, pagination, filtering, and interactive API documentation via Swagger.

---

## Features
- **JWT Authentication**: Register & login users.
- **Role-based Access**: Admin can access all tasks, normal users can only manage their own.
- **CRUD Endpoints**: Create, read, update, delete tasks.
- **Pagination**: Control results with `page` and `per_page` query parameters.
- **Filtering**: Filter tasks by completion status (`completed=true|false`).
- **Swagger Docs**: API docs available at `/apidocs`.
- **Testing**: Unit tests with `pytest` & coverage reports.

---

## Tech Stack
- **Backend**: Flask, SQLAlchemy
- **Auth**: flask-jwt-extended
- **DB**: SQLite (default), configurable for Postgres/MySQL
- **Serialization**: Marshmallow
- **Docs**: Flasgger
- **Testing**: pytest, pytest-cov

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/task-manager-api.git
cd task-manager-api
```

## **Setup & Installation**

### Create Virtual Environment
```bash
python -m venv .venv
# Activate:
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

###  Initialize Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Run the Server
```bash
flask run
```
API: http://127.0.0.1:5000

Docs: http://127.0.0.1:5000/apidocs

## API Endpoints

### Auth
| Method | Endpoint         | Description         | Auth Required |
|--------|------------------|---------------------|---------------|
| POST   | `/auth/register` | Register new user   | No            |
| POST   | `/auth/login`    | Login & get JWT     | No            |

### Tasks
| Method | Endpoint          | Description           | Auth Required |
|--------|-------------------|-----------------------|---------------|
| GET    | `/tasks`          | List tasks (paginated)| Optional      |
| GET    | `/tasks/{id}`     | Get task details      | Yes           |
| POST   | `/tasks`          | Create a new task     | Yes           |
| PUT    | `/tasks/{id}`     | Update a task         | Yes           |
| DELETE | `/tasks/{id}`     | Delete a task         | Yes           |


## Pagination & Filtering

### Pagination
You can paginate task lists by passing `page` and `per_page` query parameters.

Example:
GET /tasks?page=2&per_page=5

### Filtering by Completion Status
You can filter tasks by their `completed` status.

Examples:
`GET /tasks?completed=true`
`GET /tasks?completed=false`

## Example cURL Requests

### Register
```bash
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret123"}'
  ```
### login
```bash
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret123"}'
```
### Create Task
```bash
curl -X POST http://127.0.0.1:5000/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "description": "2L whole milk"}'
```

### List Tasks
```bash
curl -X GET "http://127.0.0.1:5000/tasks?per_page=5&page=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```
### Update Task
```bash
curl -X PUT http://127.0.0.1:5000/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

```
### Delete Task
```bash
curl -X DELETE http://127.0.0.1:5000/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Running Tests
Run all tests with coverage:
```bash
set PYTHONPATH=.  # Windows
# export PYTHONPATH=. # macOS/Linux
pytest -q --cov=app --cov-report=term-missing
```

## Project Structure

```text
app/
 ├── __init__.py
 ├── config.py
 ├── extensions.py
 ├── models.py
 ├── schemas.py
 └── resources/
     ├── auth.py
     └── tasks.py
tests/
 ├── conftest.py
 ├── test_auth.py
 └── test_tasks.py
requirements.txt
wsgi.py
README.md

