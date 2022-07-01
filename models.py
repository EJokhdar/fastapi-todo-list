from database import Base
from sqlalchemy import Column, String, Boolean, Integer, asc


class Todo(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True)
    task_name = Column(String(255), nullable=False)
    checked = Column(Boolean, default=False, nullable=True)
