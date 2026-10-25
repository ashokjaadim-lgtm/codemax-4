# Learning Notes — Module 05: Python Application Development

## Day 21: Web framework and routing
FastAPI maps HTTP requests to Python functions. An endpoint combines a path and an HTTP method, for example `GET /health`.

## Day 22: SQLite and CRUD
SQLite stores records in a local database file. This project uses parameterized SQL queries:
- Create: `INSERT`
- Read: `SELECT`
- Update: `UPDATE`
- Delete: `DELETE`

## Day 23: Authentication and validation
The `X-API-Key` header protects task endpoints. Pydantic models validate request bodies, such as requiring a title between 1 and 120 characters.

## Day 24: Testing
Pytest and FastAPI's `TestClient` check the health endpoint, missing authentication, validation errors, and task CRUD flow.

## Day 25: Documentation and delivery
FastAPI automatically provides Swagger documentation at `/docs` and ReDoc at `/redoc`. The README explains setup, endpoints, examples, and tests.

## Improvements to try
1. Add a due date field to tasks.
2. Add pagination with `offset` and `limit`.
3. Add user accounts and per-user task ownership.
4. Add database migrations.
5. Deploy behind HTTPS with a production authentication method.
