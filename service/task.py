from dataclasses import dataclass

from exception import TaskNotFound
from repository import TaskRepository, CacheTask
from schemas import Task, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: CacheTask

    def get_tasks(self, user_id: int) -> list[Task]:
        if cache_tasks := self.task_cache.get_tasks():
            return cache_tasks
        else:
            tasks = self.task_repository.get_tasks(user_id=user_id)
        tasks_schema = [Task.model_validate(task) for task in tasks]
        self.task_cache.set_tasks(tasks_schema)
        return tasks_schema

    def create_task(self, body: TaskCreateSchema, user_id: int) -> Task:
        task_id = self.task_repository.create_task(body, user_id)
        task = self.task_repository.get_task(task_id)
        return Task.model_validate(task)

    def update_name(self, task_id, name: str, user_id: int) -> Task:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        task = self.task_repository.update_name(task_id=task_id, name=name)
        return Task.model_validate(task)

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        self.task_repository.delete_task(task_id=task_id, user_id=user_id)


