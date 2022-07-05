import models
import schema
import redis
import json
import ast
from sqlalchemy.orm import Session
from redis import Redis
from fastapi import HTTPException, status
from schema import TodoResponse

CACHE_KEY_TEMPLATE = "task:{task_id}"


def get_all_tasks(db: Session):
    return db.query(models.Todo).all()


def read_from_redis(key: str, redis: Redis):
    byte_response = redis.get(key)
    if byte_response is None:
        return None
    else:
        return json.loads(byte_response.decode("UTF-8"))


def get_task(db: Session, task_id: int, redis: Redis):
    cache_key = CACHE_KEY_TEMPLATE.format(task_id=task_id)
    response = read_from_redis(cache_key, redis)
    if response is not None:
        print("cache hit!!")
        return response

    print("cache miss!")
    task = db.query(models.Todo).filter(
        models.Todo.task_id == task_id).first()
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    redis.set(cache_key, TodoResponse.from_orm(task).json())

    return task


def create_task(db: Session, task: schema.TodoRequest):
    db_task = models.Todo(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, redis: Redis):
    cache_key = CACHE_KEY_TEMPLATE.format(task_id=task_id)
    redis.delete(cache_key)

    task_delete = db.query(models.Todo).filter(
        models.Todo.task_id == task_id).first()

    if task_delete is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    db.delete(task_delete)
    db.commit()
    return task_delete


def update_task(db: Session, task: schema.TodoRequest, task_id: int, redis: Redis):
    cache_key = CACHE_KEY_TEMPLATE.format(task_id=task_id)
    redis.delete(cache_key)

    task_update = db.query(models.Todo).filter(
        models.Todo.task_id == task_id).first()
    task_update.task_name = task.task_name
    task_update.checked = task.checked

    db.commit()
    return task_update


def toggle_task(db: Session, task_id: int, redis: Redis):
    cache_key = CACHE_KEY_TEMPLATE.format(task_id=task_id)
    redis.delete(cache_key)

    toggled_task = db.query(models.Todo).filter(
        models.Todo.task_id == task_id).first()
    toggled_task.checked = not toggled_task.checked

    db.commit()
    return toggled_task
