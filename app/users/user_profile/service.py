from dataclasses import dataclass
from fastapi import HTTPException
from app.users.user_profile.repository import UserRepository
from app.users.auth.service import AuthService
from app.users.user_profile.schema import UserCreateSchema, UserSettingsSchema
from app.users.auth.schema import UserLoginSchema


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, username: str, password: str, work_duration: int = 25,
                          short_break_duration: int = 5, long_break_duration: int = 20) -> UserLoginSchema:
        user_data_create = UserCreateSchema(username=username, password=password, work_duration=work_duration,
                                            short_break_duration=short_break_duration, long_break_duration=long_break_duration)
        try_user_search = await self.user_repository.get_user_by_username(username=username)
        if try_user_search:
            raise HTTPException(status_code=400, detail='Пользователь с таким именем уже существует')
        user = await self.user_repository.create_user(user_data_create)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    async def get_settings_user(self, user_id: int) -> UserSettingsSchema:
        user_data = await self.user_repository.get_user(user_id=user_id)
        settings = UserSettingsSchema(username=user_data.username, work_duration=user_data.work_duration,
                                      short_break_duration=user_data.short_break_duration, long_break_duration=user_data.long_break_duration)
        return settings

    async def set_settings_user(self, user_id, user_data: UserSettingsSchema):
        try:
            user_settings = await self.user_repository.update_user_settings(user_id=user_id, user_data=user_data)
            return user_settings
        except Exception as e:
            return {'error': e}
