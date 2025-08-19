from fastapi import APIRouter, Depends
from app.users.user_profile.service import UserService
from app.users.user_profile.schema import UserCreateSchema
from app.users.auth.schema import UserLoginSchema
from app.dependency import get_user_service

router = APIRouter(prefix='/user', tags=['user'])


@router.post('', response_model=UserLoginSchema)
async def create_user(body: UserCreateSchema, user_service: UserService = Depends(get_user_service)):
    return await user_service.create_user(body.username, body.password)