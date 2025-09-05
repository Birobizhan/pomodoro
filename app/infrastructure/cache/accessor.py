from redis import asyncio as redis
from app.settings import Settings


def get_redis_connection() -> redis.Redis:
    """Функция для подключения к редису"""
    settings = Settings()
    return redis.Redis(host=settings.CACHE_HOST, port=settings.CACHE_PORT, db=settings.CACHE_DB)
