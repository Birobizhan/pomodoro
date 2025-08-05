from pydantic_settings import BaseSettings
from environs import Env
env = Env()
env.read_env('.local.env')


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT = 5432
    DB_USER = env('DB_USER')
    DB_PASSWORD = env('DB_PASSWORD')
    DB_NAME = env('DB_NAME')
    CACHE_HOST = 'localhost'
    CACHE_PORT = 6379
    CACHE_DB = 0
