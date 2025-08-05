from dataclasses import dataclass

from repository import TaskRepository, CacheTask
from shemas.tasks import Task


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: CacheTask

    def get_tasks(self):
        if tasks := self.task_cache.get_tasks():
            return tasks
        else:
            tasks = self.task_repository.get_tasks()
        task_schema = [Task.model_validate(task) for task in tasks]
        self.task_cache.set_tasks(task_schema)
        return task_schema
