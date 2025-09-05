from dataclasses import dataclass
from fastapi import HTTPException
from app.exception import TaskNotFound
from app.tasks.repository import TaskRepository, CacheTask
from app.tasks.schema import Task, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: CacheTask

    async def get_tasks(self, user_id: int) -> list[Task]:
        """Получение задач пользователя из кеша, если есть или из бд"""
        if cache_tasks := await self.task_cache.get_tasks(user_id=user_id):
            return cache_tasks
        else:
            tasks = await self.task_repository.get_tasks(user_id=user_id)
        tasks_schema = [Task.model_validate(task) for task in tasks]
        await self.task_cache.set_tasks(tasks_schema)
        return tasks_schema

    async def get_task_by_id(self, task_id: int, user_id: int):
        """Метод получения задачи по id"""
        task = await self.task_repository.get_user_task(task_id=task_id, user_id=user_id)
        if task:
            return Task.model_validate(task)
        raise HTTPException(status_code=404, detail='Задачи с таким id не существует')

    async def create_task(self, body: TaskCreateSchema, user_id: int) -> Task:
        """Метод создания задачи"""
        task_id = await self.task_repository.create_task(body, user_id)
        task = await self.task_repository.get_task(task_id)
        await self.task_cache.set_task(Task.model_validate(task))
        return Task.model_validate(task)

    async def update_name(self, task_id, name: str, user_id: int) -> Task:
        """Метод обновления названия задачи"""
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        task = await self.task_repository.update_name(task_id=task_id, name=name)
        await self.task_cache.update_task_for_user(updated_task=Task.model_validate(task))
        return Task.model_validate(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        """Метод удаления задачи"""
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        await self.task_repository.delete_task(task_id=task_id, user_id=user_id)
        await self.task_cache.delete_task(task_id=task_id, user_id=user_id)
