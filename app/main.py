from fastapi import FastAPI, Request
import logging
import time
from app.tasks.handlers import router as task_router
from app.handlers import ping_router
from app.users.user_profile.handlers import router as user_router
from app.users.auth.handlers import router as auth_router
from app.timer.handlers import router as timer_router

routers = [task_router, ping_router, user_router, auth_router, timer_router]
app = FastAPI()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("middleware.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


for router in routers:
    app.include_router(router)


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    """Функция логирования, если ошибок нет то передает всю информацию о запросе, иначе ошибку"""
    try:
        start_time = time.time()
        logger.info(f"Запрос: {request.method} {request.url}")
        logger.info(f"Заголовки: {request.headers}")

        if request.method in ["POST", "PUT"]:
            body = await request.body()
            logger.info(f"Тело запроса: {body.decode()}")

        response = await call_next(request)

        process_time = time.time() - start_time
        logger.info(f"Ответ: {response.status_code}")
        logger.info(f"Время выполнения: {process_time:.2f} секунд")

        return response
    except Exception as e:
        logger.error(f'Ошибка {str(e)}')
        raise
