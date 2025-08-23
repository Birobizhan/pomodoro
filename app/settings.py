from pydantic_settings import BaseSettings
from environs import Env
env = Env()
env.read_env('.local.env')


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = env('DB_USER')
    DB_PASSWORD: str = env('DB_PASSWORD')
    DB_DRIVER: str = 'postgresql+asyncpg'
    DB_NAME: str = env('DB_NAME')
    CACHE_HOST: str = 'localhost'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    JWT_SECRET_KEY: str = env('JWT_SECRET_KEY')
    JWT_ENCODE_ALGORITHM: str = env('JWT_ENCODE_ALGORITHM')
    GOOGLE_CLIENT_ID: str = env('GOOGLE_CLIENT_ID')
    GOOGLE_SECRET_KEY: str = env('GOOGLE_SECRET_KEY')
    GOOGLE_REDIRECT_URI: str = env('GOOGLE_REDIRECT_URI')
    GOOGLE_TOKEN_URL: str = 'https://accounts.google.com/o/oauth2/token'
    YANDEX_CLIENT_ID: str = env('YANDEX_CLIENT_ID')
    YANDEX_SECRET_KEY: str = env('YANDEX_SECRET_KEY')
    YANDEX_REDIRECT_URI: str = env('YANDEX_REDIRECT_URI')
    YANDEX_TOKEN_URL: str = 'https://oauth.yandex.ru/token'
    DB_TEST_URL: str = env('DB_TEST_URL')
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7
    CELERY_BROKER_URL: str = env('CELERY_BROKER_URL')
    from_email: str = env('from_email')
    SMTP_PORT: int = 465
    SMTP_HOST: str = 'smtp.gmail.com'
    SMTP_PASSWORD: str = env('SMTP_PASSWORD')

    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def google_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"

    @property
    def yandex_redirect_url(self) -> str:
        return f'https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&redirect_uri{self.YANDEX_REDIRECT_URI}&scope=login:info'