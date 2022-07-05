from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from database import Base
from main import app
from dependencies import get_db_session
from dependencies import get_redis_client
import pytest
from redis import Redis

engine = create_engine(
    "postgresql://postgres:332001@localhost/test_todo_db", echo=True)
Base = declarative_base()
TestSessionLocal = sessionmaker(engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db_session():
        try:
            db = TestSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db_session] = override_get_db_session
    client = TestClient(app)

    yield client


@pytest.fixture
def redis():
    def override_get_redis_client():
        redis_client = Redis(host="localhost", port=6379, db=0)
        yield redis_client
    app.dependency_overrides[get_redis_client] = override_get_redis_client
    redis = Redis(host="localhost", port=6379, db=0)
    yield redis


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
