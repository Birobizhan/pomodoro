import pytest
import pytest_asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from app.settings import Settings
from app.infrastructure.database.database import Base
from environs import Env

env = Env()
env.read_env('.local.env')


@pytest.fixture
def settings():
    return Settings()


@pytest_asyncio.fixture(scope="function")
async def async_engine_test():
    engine = create_async_engine(url=env('DB_TEST_URL'), echo=False)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def init_db_for_tests(async_engine_test: AsyncEngine):
    async with async_engine_test.connect() as connection:
        async with connection.begin():
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)
    yield




@pytest_asyncio.fixture(scope="function")
async def get_db_session(async_engine_test: AsyncEngine):
    connection = await async_engine_test.connect()
    transaction = await connection.begin()
    AsyncSessionLocal = sessionmaker(
        async_engine_test, class_=AsyncSession, expire_on_commit=False
    )
    session = AsyncSessionLocal(bind=connection)

    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()