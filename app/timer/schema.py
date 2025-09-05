from pydantic import BaseModel


class TaskTimer(BaseModel):
    id: int
    name: str
    pomodoro_count: int
    time_remaining: str
