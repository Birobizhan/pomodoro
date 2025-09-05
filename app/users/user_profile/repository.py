from dataclasses import dataclass

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.user_profile.models import UserProfile
from app.users.user_profile.schema import UserCreateSchema, UserSettingsSchema


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def get_user_by_email(self, email: str) -> UserProfile | None:
        """Получение пользоавтеля по email"""
        query = select(UserProfile).where(UserProfile.email == email)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def create_user(self, user_data: UserCreateSchema) -> UserProfile:
        """Создание пользователя"""
        query = insert(UserProfile).values(**user_data.dict(exclude_none=True)).returning(UserProfile.id)
        async with self.db_session as session:
            user_id: int = (await session.execute(query)).scalar()
            await session.commit()
            await session.flush()
            return await self.get_user(user_id)

    async def get_user(self, user_id) -> UserProfile | None:
        """Получение пользователя по id"""
        query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserProfile | None:
        """Получение пользователя по username"""
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def update_user_settings(self, user_id, user_data: UserSettingsSchema) -> UserProfile | None:
        """Обновление настроек пользователя"""
        query = update(UserProfile).where(UserProfile.id == user_id).values(username=user_data.username, work_duration=user_data.work_duration,
                                                                            short_break_duration=user_data.short_break_duration, long_break_duration=user_data.long_break_duration)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
            return await self.get_user(user_id)
