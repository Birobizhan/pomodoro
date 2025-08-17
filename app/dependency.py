from typing import Annotated
from fastapi import Depends, security, Security, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.client import GoogleClient, YandexClient
from app.infrastructure.database import get_db_session
from app.exception import TokenExpiredException, TokenINCorrectException
from app.repository import TaskRepository, CacheTask, UserRepository
from app.infrastructure.cache import get_redis_connection
from app.service import TaskService, UserService
from app.service import AuthService
from app.settings import Settings


async def get_tasks_repository(db_session: AsyncSession = Depends(get_db_session)) -> TaskRepository:
    return TaskRepository(db_session)


async def get_cache_repository() -> CacheTask:
    redis_connection = get_redis_connection()
    return CacheTask(redis_connection)


async def get_task_service(task_repository: TaskRepository = Depends(get_tasks_repository), task_cache: CacheTask = Depends(get_cache_repository)) -> TaskService:
    return TaskService(task_repository=task_repository, task_cache=task_cache)


async def get_user_repository(db_session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_yandex_client() -> YandexClient:
    return YandexClient(settings=Settings())


async def get_google_client() -> GoogleClient:
    return GoogleClient(settings=Settings())


async def get_auth_service(google_client: Annotated[GoogleClient, Depends(get_google_client)], yandex_client: Annotated[YandexClient, Depends(get_yandex_client)], user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository=user_repository, settings=Settings(), google_client=google_client, yandex_client=yandex_client)


async def get_user_service(user_repository: UserRepository = Depends(get_user_repository), auth_service: AuthService = Depends(get_auth_service)):
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


async def get_request_user_id(auth_service: AuthService = Depends(get_auth_service),
                        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)) -> int:

    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpiredException:
        raise HTTPException(status_code=401, detail='Unauthorized')
    except TokenINCorrectException:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return user_id

