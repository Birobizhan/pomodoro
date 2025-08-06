from fastapi import Depends
from database import get_db_session
from repository import TaskRepository, CacheTask, UserRepository
from cache import get_redis_connection
from service import TaskService, UserService
from sqlalchemy.orm import Session
from service import AuthService


def get_tasks_repository(db_session: Session = Depends(get_db_session)) -> TaskRepository:
    return TaskRepository(db_session)


def get_cache_repository() -> CacheTask:
    redis_connection = get_redis_connection()
    return CacheTask(redis_connection)


def get_task_service(task_repository: TaskRepository = Depends(get_tasks_repository), task_cache: CacheTask = Depends(get_cache_repository)) -> TaskService:
    return TaskService(task_repository=get_tasks_repository(), task_cache=get_cache_repository())


def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository=user_repository)


def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository=user_repository)


