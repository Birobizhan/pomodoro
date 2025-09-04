from pydantic import BaseModel, model_validator, ConfigDict

from app.tasks.models import TaskStatus


class Task(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int | None = None
    user_id: int
    status: TaskStatus = TaskStatus.PLANNED

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def check_name_pomodoro_count(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError('name and pomodoro count is None')
        return self


class TaskCreateSchema(BaseModel):
    name: str | None = None
    pomodoro_count: int | None = None
