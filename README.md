# Task Manager API

A scalable task management backend built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **JWT Authentication**.

---

# Features

* User Registration & Login
* JWT Authentication
* Organization Management
* Project Management
* Task Creation & Assignment
* Task Status Tracking
* Role-Based Access Support
* PostgreSQL Integration
* FastAPI Swagger Documentation
* SQLAlchemy ORM

---

# Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT Authentication
* Uvicorn

---

# Project Structure

```bash
app/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── dependencies.py
├── config.py
│
├── routes/
│   └── auth.py
│
├── utils/
│   ├── hashing.py
│   └── token.py
│
└── __init__.py
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/task-manager-api.git

cd task-manager-api
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Linux / Mac

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory.

```env
SECRET_KEY=your_secret_key_here

DATABASE_URL=postgresql://postgres:password@localhost/task_manager

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# PostgreSQL Setup

Create database manually:

```sql
CREATE DATABASE task_manager;
```

---

# Run the Application

```bash
uvicorn app.main:app --reload
```

Application runs at:

```bash
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI provides automatic interactive documentation.

## Swagger UI

```bash
http://127.0.0.1:8000/docs
```

## ReDoc

```bash
http://127.0.0.1:8000/redoc
```

---

# Authentication

This API uses JWT Bearer Authentication.

After login:

1. Copy the access token
2. Open Swagger UI
3. Click **Authorize**
4. Enter:

```text
Bearer your_access_token
```

---

# API Endpoints

# Authentication

| Method | Endpoint    | Description       |
| ------ | ----------- | ----------------- |
| POST   | `/register` | Register new user |
| POST   | `/login`    | Login user        |

---

# Organizations

| Method | Endpoint                  | Description              |
| ------ | ------------------------- | ------------------------ |
| POST   | `/organizations`          | Create organization      |
| GET    | `/organizations/{org_id}` | Get organization details |

---

# Projects

| Method | Endpoint                 | Description         |
| ------ | ------------------------ | ------------------- |
| POST   | `/projects`              | Create project      |
| GET    | `/projects/{project_id}` | Get project details |

---

# Tasks

| Method | Endpoint           | Description        |
| ------ | ------------------ | ------------------ |
| POST   | `/tasks`           | Create task        |
| GET    | `/tasks`           | Get tasks          |
| PATCH  | `/tasks/{task_id}` | Update task status |

---

# Task Status

Supported task statuses:

```text
TODO
IN_PROGRESS
DONE
```

---

# Example Requests

## Register User

```http
POST /register
```

```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

---

## Login User

```http
POST /login
```

```json
{
  "username": "john@example.com",
  "password": "password123"
}
```

---

## Create Organization

```http
POST /organizations
Authorization: Bearer <token>
```

```json
{
  "name": "Acme Inc"
}
```

---

## Create Project

```http
POST /projects
Authorization: Bearer <token>
```

```json
{
  "name": "Backend API",
  "org_id": 1
}
```

---

## Create Task

```http
POST /tasks
Authorization: Bearer <token>
```

```json
{
  "title": "Implement JWT Authentication",
  "description": "Add login functionality",
  "project_id": 1,
  "assigned_user_id": 2
}
```

---

## Update Task Status

```http
PATCH /tasks/1
Authorization: Bearer <token>
```

```json
{
  "status": "DONE"
}
```

---

# Security Features

* Password Hashing
* JWT Token Authentication
* Protected Routes
* Organization-Based Authorization
* User Access Validation

---

# Future Improvements

* Role-Based Permissions
* Task Comments
* File Uploads
* Notifications
* WebSocket Support
* Docker Support
* CI/CD Integration
* Unit & Integration Tests
* Async SQLAlchemy
* Redis Caching

---

# Running Tests

```bash
pytest
```

---

# Production Recommendations

* Use Alembic Migrations
* Add Logging
* Configure HTTPS
* Add Rate Limiting
* Use Environment-Based Config
* Enable Monitoring
* Use Gunicorn + Nginx

---

# License

MIT License

---

# Author

Built with FastAPI and PostgreSQL.
