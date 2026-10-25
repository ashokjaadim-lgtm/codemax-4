# Python Application Development — Task Manager REST API

A beginner-friendly project for Module 05 (Days 21–25). It demonstrates a documented Python REST API using **FastAPI**, **SQLite**, request validation, API-key authentication, CRUD operations, and tests.

## Features

- REST endpoints to create, read, update, and delete tasks
- SQLite database storage (created automatically)
- Simple API-key authentication using the `X-API-Key` header
- Pydantic request validation
- Filter tasks by completion status and limit the results
- Automatic interactive API documentation
- Pytest tests for authentication, validation, and CRUD

## Project structure

```text
python-application-development/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── tests/
    └── test_main.py
```

## 1. Install Python

Use Python 3.10 or newer. Verify:

```bash
python --version
```

## 2. Create and activate a virtual environment

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## 4. Configure the API key

The app has a development key by default: `dev-secret-key-change-me`.

For local practice, you can run it directly. To use your own key, set environment variables before starting.

### Windows PowerShell

```powershell
$env:API_KEY="my-local-secret"
$env:DATABASE_PATH="tasks.db"
```

### macOS / Linux

```bash
export API_KEY="my-local-secret"
export DATABASE_PATH="tasks.db"
```

Do not commit real secrets to GitHub. `.env.example` is only a template; this project does not automatically load `.env` files.

## 5. Run the API

```bash
uvicorn main:app --reload
```

Open these pages in your browser:

- Home: http://127.0.0.1:8000/
- Interactive Swagger docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

## API authentication

For protected endpoints, send this header:

```text
X-API-Key: dev-secret-key-change-me
```

In Swagger (`/docs`), select an endpoint and add the `X-API-Key` header in the request headers. For a production app, replace this demo API-key approach with a proper authentication system and store secrets securely.

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks |
| GET | `/tasks/{task_id}` | Get one task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

All `/tasks` endpoints require the API-key header.

### Create task example

Request body:

```json
{
  "title": "Complete Python module",
  "description": "Build and document a REST API",
  "completed": false
}
```

Example using curl:

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret-key-change-me" \
  -d '{"title":"Complete Python module","description":"Build a REST API","completed":false}'
```

### List and filter tasks

```bash
curl "http://127.0.0.1:8000/tasks?completed=false&limit=20" \
  -H "X-API-Key: dev-secret-key-change-me"
```

### Update a task

```bash
curl -X PUT "http://127.0.0.1:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret-key-change-me" \
  -d '{"completed":true}'
```

### Delete a task

```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1" \
  -H "X-API-Key: dev-secret-key-change-me"
```

## Run tests

```bash
pytest -q
```

## Learning notes

- **REST API:** a web interface that uses HTTP methods to work with resources.
- **Routing:** maps a URL and HTTP method to a Python function.
- **Endpoint:** one API URL, such as `GET /tasks`.
- **CRUD:** Create, Read, Update, Delete.
- **SQLite:** a lightweight database stored in a local file.
- **Schema validation:** checks request data types and constraints before processing.
- **Authentication:** verifies that the request includes the expected API key.
- **HTTP status codes:** `200` success, `201` created, `204` deleted, `401` unauthorized, `404` not found, `422` validation error.

## Notes and limitations

This is an educational starter project, not a production-ready service. The API key is a simple shared secret; use HTTPS and a stronger authentication design before deploying publicly. Change the default key and never publish real secrets.
