from fastapi import FastAPI, status, HTTPException, Depends
from database import SessionLocal
from typing import List
from schema import TodoResponse, TodoRequest
from sqlalchemy.orm import Session
import models
import crud


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tasks", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
def read_all_tasks(db: Session = Depends(get_db)):
    return crud.get_all_tasks(db)


@app.get("/tasks/{task_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def read_task(task_id: int, db: Session = Depends(get_db)):
    return crud.get_task(db=db, task_id=task_id)


@app.post("/tasks", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_tasks(task: TodoRequest, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)


@app.delete("/tasks/{task_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return crud.delete_task(db=db, task_id=task_id)


@app.put("/tasks/{task_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: TodoRequest, db: Session = Depends(get_db)):
    return crud.update_task(db=db, task=task, task_id=task_id)


@app.post("/tasks/{task_id}/toggle", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def toggle_task(task_id: int, db: Session = Depends(get_db)):
    return crud.toggle_task(db=db, task_id=task_id)
