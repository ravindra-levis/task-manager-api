# Task Manager API

A FastAPI-based task management system with user authentication, organizations, projects, and tasks.

## Features
- User registration and JWT-based login
- Create and manage organizations, projects, and tasks
- Task status tracking (TODO, IN_PROGRESS, DONE)
- Secure API with authentication

## Setup
1. Clone the repo and navigate to the directory.
2. Install dependencies: `pip install -r requirements.txt`
3. Set up PostgreSQL database and update `.env` with your `DATABASE_URL`.
4. Run the app: `uvicorn app.main:app --reload`
5. Access API docs at `http://localhost:8000/docs`

## API Endpoints
- POST /register: Register a new user
- POST /login: Login and get JWT token
- GET /organizations/{org_id}: Get organization (authenticated)
- POST /organizations/: Create organization
- POST /organizations/{org_id}/projects: Create project
- POST /organizations/{org_id}/projects/{prj_id}/tasks/: Create task
- GET /projects/{prj_id}/tasks/{task_id}: Get task
- PATCH /projects/{prj_id}/tasks/{task_id}: Update task status
- GET /tasks/: List tasks (filter by status)

## Environment Variables
- SECRET_KEY: JWT secret
- DATABASE_URL: PostgreSQL connection string