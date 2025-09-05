import json
from redis import asyncio as Redis
from app.tasks.schema import Task


class CacheTask:
    def __init__(self, redis: Redis.Redis):
        self.redis = redis

    async def get_tasks(self, user_id: int) -> list[Task]:
        """Получение всех задач пользователя что есть в кеше"""
        user_tasks_key: str = f"user_tasks:{user_id}"
        async with self.redis as r:
            task_json_list = await r.lrange(user_tasks_key, 0, -1)
            return [Task.model_validate_json(task_json) for task_json in task_json_list]

    async def set_tasks(self, tasks: list[Task]) -> None:
        """Запись нескольких задач в кеш"""
        for task in tasks:
            user_tasks_key: str = f"user_tasks:{task.user_id}"
            async with self.redis as r:
                await r.lpush(user_tasks_key, task.model_dump_json())

    async def set_task(self, task: Task) -> None:
        """Запись одной задачи в кеш, используется при создании задачи"""
        user_tasks_key: str = f"user_tasks:{task.user_id}"
        async with self.redis as r:
            await r.lpush(user_tasks_key, task.model_dump_json())

    async def delete_task(self, task_id: int, user_id: int) -> bool:
        """Удаление задачи из кеша"""
        user_tasks_key = f'users_tasks{user_id}'
        async with self.redis as redis:
            task_json_list = await redis.lrange(user_tasks_key, 0, -1)
            task_to_remove_json = None
            for task_json in task_json_list:
                task = Task.model_validate_json(task_json)
                if task.id == task_id:
                    task_to_remove_json = task_json
                    break
            if task_to_remove_json:
                removed_count = await redis.lrem(user_tasks_key, 1, task_to_remove_json)
                return removed_count > 0
            return False

    async def update_task_for_user(self, updated_task: Task) -> bool:
        """Обновление задачи в кеше"""
        user_tasks_key = f"user_tasks:{updated_task.user_id}"
        async with self.redis as r:
            task_json_list = await r.lrange(user_tasks_key, 0, -1)
            found_index = -1
            old_task_json = None
            for i, task_json in enumerate(task_json_list):
                task = Task.model_validate_json(task_json)
                if task.id == updated_task.id:
                    found_index = i
                    old_task_json = task_json
                    break

            if found_index != -1 and old_task_json:
                await r.lrem(user_tasks_key, 1, old_task_json)
                await r.lpush(user_tasks_key, updated_task.model_dump_json())
                return True
            return False
