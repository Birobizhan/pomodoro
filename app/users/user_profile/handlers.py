from typing import Annotated

from fastapi import APIRouter, Depends
from app.users.user_profile.service import UserService
from app.users.user_profile.schema import UserCreateBasicSchema, UserSettingsSchema
from app.users.auth.schema import UserLoginSchema
from app.dependency import get_user_service, get_request_user_id

router = APIRouter(prefix='/user', tags=['user'])


@router.post('', response_model=UserLoginSchema)
async def create_user(body: UserCreateBasicSchema, user_service: UserService = Depends(get_user_service)):
    """Ручка создания пользователя"""
    return await user_service.create_user(username=body.username, password=body.password,
                                          work_duration=body.work_duration,
                                          short_break_duration=body.short_break_duration,
                                          long_break_duration=body.long_break_duration)


@router.get('/settings')
async def get_settings(user_service: Annotated[UserService, Depends(get_user_service)],
                       user_id: int = Depends(get_request_user_id)):
    """Ручка получения настроек пользователя"""
    return await user_service.get_settings_user(user_id=user_id)


@router.patch('/settings')
async def set_settings(body: UserSettingsSchema, user_service: Annotated[UserService, Depends(get_user_service)],
                       user_id: int = Depends(get_request_user_id)):
    """Ручка для изменения настроек пользователя"""
    await user_service.set_settings_user(user_id=user_id, user_data=body)
