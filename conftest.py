from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from database import Base
from main import app, get_db
import pytest

engine = create_engine(
    "postgresql://postgres:332001@localhost/test_todo_db", echo=True)
Base = declarative_base()
TestSessionLocal = sessionmaker(engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        try:
            db = TestSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
def create_delete_task(client):
    request = client.post(
        "/tasks",
        json={"task_name": "test code", "checked": False}
    )

    yield request

    task = request.json()
    task_id = task["task_id"]
    task_name = task["task_name"]
    task_checked = task["checked"]

    response = client.delete(
        f"/tasks/{task_id}",
        json={"task_name": task_name, "checked": task_checked}
    )
