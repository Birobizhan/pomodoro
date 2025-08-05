import redis


def get_redis_connection() -> redis.Redis:
    return redis.Redis(host='localhost', port=6379, db=0)


def set_pomodoro_count():
    redis = get_redis_connection()
    redis.set("pomodoro_count", 1)
