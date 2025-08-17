from dataclasses import dataclass

from app.exception import TaskNotFound
from app.repository import TaskRepository, CacheTask
from app.schemas import Task, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: CacheTask

    async def get_tasks(self, user_id: int) -> list[Task]:
        if cache_tasks := await self.task_cache.get_tasks():
            return cache_tasks
        else:
            tasks = await self.task_repository.get_tasks(user_id=user_id)
        tasks_schema = [Task.model_validate(task) for task in tasks]
        await self.task_cache.set_tasks(tasks_schema)
        return tasks_schema

    async def create_task(self, body: TaskCreateSchema, user_id: int) -> Task:
        task_id = await self.task_repository.create_task(body, user_id)
        task = await self.task_repository.get_task(task_id)
        return Task.model_validate(task)

    async def update_name(self, task_id, name: str, user_id: int) -> Task:
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        task = await self.task_repository.update_name(task_id=task_id, name=name)
        return Task.model_validate(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        await self.task_repository.delete_task(task_id=task_id, user_id=user_id)
