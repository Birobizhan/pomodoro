import redis
from settings import Settings


def get_redis_connection() -> redis.Redis:
    settings = Settings()
    return redis.Redis(host=settings.CACHE_HOST, port=settings.CACHE_PORT, db=settings.CACHE_DB)


def set_pomodoro_count():
    redis = get_redis_connection()
    redis.set("pomodoro_count", 1)
