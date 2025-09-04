from pydantic import BaseModel
from app.tasks.models import TaskStatus


class TaskTimer(BaseModel):
    id: int
    name: str
    pomodoro_count: int
    time_remaining: str
