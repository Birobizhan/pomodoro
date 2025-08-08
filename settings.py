from pydantic_settings import BaseSettings
from environs import Env
env = Env()
env.read_env('.local.env')


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = env('DB_USER')
    DB_PASSWORD: str = env('DB_PASSWORD')
    DB_DRIVER: str = 'postgresql+psycopg2'
    DB_NAME: str = env('DB_NAME')
    CACHE_HOST: str = 'localhost'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    JWT_SECRET_KEY: str = env('JWT_SECRET_KEY')
    JWT_ENCODE_ALGORITHM: str = env('JWT_ENCODE_ALGORITHM')

    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
