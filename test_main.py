import os
import tempfile

# Configure the database before importing the application.
db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
db_file.close()
os.environ["DATABASE_PATH"] = db_file.name
os.environ["API_KEY"] = "test-api-key"

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
HEADERS = {"X-API-Key": "test-api-key"}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_authentication_required():
    response = client.get("/tasks")
    assert response.status_code == 401


def test_task_crud():
    created = client.post(
        "/tasks",
        headers=HEADERS,
        json={"title": "Learn FastAPI", "description": "Build a REST API"},
    )
    assert created.status_code == 201
    task = created.json()
    task_id = task["id"]
    assert task["title"] == "Learn FastAPI"
    assert task["completed"] is False

    fetched = client.get(f"/tasks/{task_id}", headers=HEADERS)
    assert fetched.status_code == 200
    assert fetched.json()["id"] == task_id

    updated = client.put(
        f"/tasks/{task_id}",
        headers=HEADERS,
        json={"completed": True},
    )
    assert updated.status_code == 200
    assert updated.json()["completed"] is True

    listed = client.get("/tasks?completed=true", headers=HEADERS)
    assert listed.status_code == 200
    assert any(item["id"] == task_id for item in listed.json())

    deleted = client.delete(f"/tasks/{task_id}", headers=HEADERS)
    assert deleted.status_code == 204

    missing = client.get(f"/tasks/{task_id}", headers=HEADERS)
    assert missing.status_code == 404


def test_schema_validation():
    response = client.post(
        "/tasks",
        headers=HEADERS,
        json={"title": ""},
    )
    assert response.status_code == 422
