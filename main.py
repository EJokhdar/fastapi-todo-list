from fastapi import FastAPI, status, HTTPException, Depends
from database import SessionLocal
from typing import List
from schema import TodoResponse, TodoRequest
from sqlalchemy.orm import Session
from redis import Redis
from dependencies import get_db_session
from dependencies import get_redis_client
import models
import crud


app = FastAPI()


@app.get("/tasks", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
def get_all_tasks(db: Session = Depends(get_db_session)):
    return crud.get_all_tasks(db)


@app.get("/tasks/{task_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def get_task(task_id: int, db: Session = Depends(get_db_session), redis: Redis = Depends(get_redis_client)):
    return crud.get_task(db=db, task_id=task_id, redis=redis)


@app.post("/tasks", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_tasks(task: TodoRequest, db: Session = Depends(get_db_session)):
    return crud.create_task(db=db, task=task)


@app.delete("/tasks/{task_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db_session), redis: Redis = Depends(get_redis_client)):
    return crud.delete_task(db=db, task_id=task_id, redis=redis)


@app.put("/tasks/{task_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: TodoRequest, db: Session = Depends(get_db_session), redis: Redis = Depends(get_redis_client)):
    return crud.update_task(db=db, task=task, task_id=task_id, redis=redis)


@app.post("/tasks/{task_id}/toggle", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def toggle_task(task_id: int, db: Session = Depends(get_db_session), redis: Redis = Depends(get_redis_client)):
    return crud.toggle_task(db=db, task_id=task_id, redis=redis)
