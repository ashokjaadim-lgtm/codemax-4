import os
import sqlite3
from contextlib import contextmanager
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from pydantic import BaseModel, Field

APP_NAME = "Task Manager REST API"
DATABASE_PATH = os.getenv("DATABASE_PATH", "tasks.db")
API_KEY = os.getenv("API_KEY", "dev-secret-key-change-me")

app = FastAPI(
    title=APP_NAME,
    description="A beginner-friendly REST API demonstrating authentication, validation, SQLite CRUD, and automatic documentation.",
    version="1.0.0",
)


@contextmanager
def get_connection():
    """Open a SQLite connection and always close it."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def initialize_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        connection.commit()


initialize_database()


def require_api_key(x_api_key: Optional[str] = Header(default=None)):
    """Protect API routes with a simple API key header."""
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key. Send it in the X-API-Key header.",
        )


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120, description="Short task title")
    description: str = Field(default="", max_length=1000)
    completed: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


def row_to_task(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "completed": bool(row["completed"]),
    }


@app.get("/", tags=["General"])
def home():
    return {
        "message": "Welcome to the Task Manager REST API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["General"])
def health():
    return {"status": "ok"}


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
    tags=["Tasks"],
)
def create_task(task: TaskCreate):
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
            (task.title.strip(), task.description, int(task.completed)),
        )
        connection.commit()
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return row_to_task(row)


@app.get(
    "/tasks",
    response_model=list[TaskResponse],
    dependencies=[Depends(require_api_key)],
    tags=["Tasks"],
)
def list_tasks(
    completed: Optional[bool] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
):
    with get_connection() as connection:
        if completed is None:
            rows = connection.execute(
                "SELECT * FROM tasks ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT * FROM tasks WHERE completed = ? ORDER BY id DESC LIMIT ?",
                (int(completed), limit),
            ).fetchall()
    return [row_to_task(row) for row in rows]


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    dependencies=[Depends(require_api_key)],
    tags=["Tasks"],
)
def get_task(task_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return row_to_task(row)


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    dependencies=[Depends(require_api_key)],
    tags=["Tasks"],
)
def update_task(task_id: int, task: TaskUpdate):
    updates = task.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="Provide at least one field to update")
    if "title" in updates and updates["title"] is not None:
        updates["title"] = updates["title"].strip()
        if not updates["title"]:
            raise HTTPException(status_code=422, detail="Title cannot be blank")

    with get_connection() as connection:
        existing = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Task not found")

        values = {}
        for key, value in updates.items():
            if value is not None:
                values[key] = int(value) if key == "completed" else value

        if values:
            assignments = ", ".join(f"{column} = ?" for column in values)
            connection.execute(
                f"UPDATE tasks SET {assignments} WHERE id = ?",
                (*values.values(), task_id),
            )
            connection.commit()
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
    return row_to_task(row)


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_api_key)],
    tags=["Tasks"],
)
def delete_task(task_id: int):
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        connection.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
