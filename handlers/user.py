from fastapi import APIRouter, Depends
from service import UserService
from shemas import UserCreateSchema, UserLoginSchema
from dependency import get_user_service

router = APIRouter(prefix='/user', tags=['user'])


@router.post('', response_model=UserLoginSchema)
async def create_user(body: UserCreateSchema, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(body.username, body.password)