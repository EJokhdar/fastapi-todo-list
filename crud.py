import models
import schema
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def get_all_tasks(db: Session):
    return db.query(models.Todo).all()


def get_task(db: Session, task_id: int):
    task = db.query(models.Todo).filter(models.Todo.task_id == task_id).first()
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return task


def create_task(db: Session, task: schema.TodoRequest):
    db_task = models.Todo(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    task_delete = db.query(models.Todo).filter(
        models.Todo.task_id == task_id).first()

    if task_delete is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    db.delete(task_delete)
    db.commit()

    return task_delete


def update_task(db: Session, task: schema.TodoRequest, task_id: int):
    task_update = db.query(models.Todo).filter(
        models.Todo.task_id == task_id).first()
    task_update.task_name = task.task_name
    task_update.checked = task.checked

    db.commit()

    return task_update


def toggle_task(db: Session, task_id: int):
    task_uncheck = db.query(models.Todo).filter(
        models.Todo.task_id == task_id).first()
    task_uncheck.checked = not task_uncheck.checked

    db.commit()

    return task_uncheck
