from fastapi import APIRouter, Depends, HTTPException

from exception import UserNotFoundException, UserIncorrectPasswordException
from service import UserService, AuthService
from shemas import UserCreateSchema, UserLoginSchema
from dependency import get_user_service, get_auth_service

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=UserLoginSchema)
async def login(body: UserCreateSchema, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserIncorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)
