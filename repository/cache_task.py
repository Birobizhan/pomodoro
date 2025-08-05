import json

from redis import Redis

from shemas.tasks import Task


class CacheTask:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> list[Task]:
        with self.redis as redis:
            task_json = redis.lrange("tasks", 0, -1)
            return [Task.model_validate(json.loads(task)) for task in task_json]

    def set_tasks(self, tasks: list[Task]):
        tasks_json = [task.json() for task in tasks]
        with self.redis as redis:
            self.redis.lpush("tasks", *tasks_json)
