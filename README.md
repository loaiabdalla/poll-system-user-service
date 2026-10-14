# Poll System - User Service

A FastAPI microservice responsible for managing system users and their registration status in the Poll System.

## Architecture
- **Framework**: FastAPI (Python 3.12)
- **Database**: MySQL 8.0 (using SQLAlchemy ORM)
- **Pattern**: MVC / Layered Architecture (`Controller` -> `Service` -> `Repository` -> `Model`)
- **Validation**: Pydantic v2 Request/Response models

## Features
- Full CRUD for users (`Create`, `Read`, `Update`, `Delete`).
- Two-step user registration (`Create` user defaults to `is_registered = False`; dedicated `/register` endpoint activates registration).
- Cascading deletion: when a user is deleted, calls the Poll Service API to delete all answers submitted by this user.

## API Endpoints (Base URL: `/api/v1`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/users` | Create a new user (`is_registered=False`) |
| `GET` | `/users` | List all users (supports pagination `skip` & `limit`, and `is_registered` filter) |
| `GET` | `/users/{user_id}` | Retrieve user details by ID |
| `PUT` | `/users/{user_id}` | Update user information |
| `DELETE`| `/users/{user_id}` | Delete user + cascades answer deletion in Poll Service |
| `PATCH`| `/users/{user_id}/register` | Dedicated endpoint to switch `is_registered` to `True` |

## Environment Variables
Configured in `.env`:
- `DATABASE_URL`: MySQL connection URL (e.g. `mysql+pymysql://user_admin:user_password@localhost:3307/user_db`)
- `POLL_SERVICE_URL`: URL to Poll Service (e.g. `http://localhost:8002/api/v1`)
- `PORT`: Service port (default `8001`)

## Running Locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

## Running with Docker
```bash
docker build -t poll-user-service .
docker run -p 8001:8001 poll-user-service
```
Interactive API documentation is accessible at `http://localhost:8001/docs`.
