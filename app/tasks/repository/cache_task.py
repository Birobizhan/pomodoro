import json
from redis import asyncio as Redis
from app.tasks.schema import Task


class CacheTask:
    def __init__(self, redis: Redis.Redis):
        self.redis = redis

    async def get_tasks(self) -> list[Task]:
        async with self.redis as redis:
            task_json = await redis.lrange("tasks", 0, -1)
            return [Task.model_validate(json.loads(task)) for task in task_json]

    async def set_tasks(self, tasks: list[Task]):
        tasks_json = [task.json() for task in tasks]
        if tasks_json:
            async with self.redis as redis:
                await redis.lpush("tasks", *tasks_json)
