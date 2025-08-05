from pydantic_settings import BaseSettings
from environs import Env
env = Env()
env.read_env('.local.env')


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT = 5432
    DB_USER = env('DB_USER')
    DB_PASSWORD = env('DB_PASSWORD')
    DB_DRIVER = 'postgresql+psycopg2'
    DB_NAME = env('DB_NAME')
    CACHE_HOST = 'localhost'
    CACHE_PORT = 6379
    CACHE_DB = 0

    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
