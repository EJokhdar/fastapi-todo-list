from pydantic import BaseModel


class TodoResponse(BaseModel):
    task_id: int
    task_name: str
    checked: bool

    class Config:
        orm_mode = True


class TodoRequest(BaseModel):
    task_name: str
    checked: bool
