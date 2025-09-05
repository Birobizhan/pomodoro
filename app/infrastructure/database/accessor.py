from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.settings import Settings

settings = Settings()

engine = create_async_engine(url=settings.db_url)

AsyncSessionFactory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def get_db_session() -> AsyncSession:
    """Функция для получения сессии асинхронной базы данных"""
    async with AsyncSessionFactory() as session:
        yield session
