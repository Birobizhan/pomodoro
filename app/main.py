from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.dependency import get_broker_consumer
from app.tasks.handlers import router as task_router
from app.handlers import ping_router
from app.users.user_profile.handlers import router as user_router
from app.users.auth.handlers import router as auth_router

routers = [task_router, ping_router, user_router, auth_router]


@asynccontextmanager
async def lifespan(app: FastAPI):
    broker_consumer = await get_broker_consumer()
    await broker_consumer.consume_callback_message()
    yield


app = FastAPI(lifespan=lifespan)

for router in routers:
    app.include_router(router)