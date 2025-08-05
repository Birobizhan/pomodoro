from fastapi import Depends
from database import get_db_session
from repository import TaskRepository, CacheTask
from cache import get_redis_connection
from service import TaskService


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_cache_repository() -> CacheTask:
    redis_connection = get_redis_connection()
    return CacheTask(redis_connection)


def get_task_service(task_repository: TaskRepository = Depends(get_tasks_repository), task_cache: CacheTask = Depends(get_cache_repository)) -> TaskService:
    return TaskService(task_repository=get_tasks_repository(), task_cache=get_cache_repository())