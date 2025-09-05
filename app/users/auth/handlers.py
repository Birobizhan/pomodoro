from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from typing import Annotated
from app.exception import UserNotFoundException, UserIncorrectPasswordException
from app.users.auth.service import AuthService
from app.users.user_profile.schema import UserCreateSchema, UserLoginProcessSchema
from app.users.auth.schema import UserLoginSchema
from app.dependency import get_auth_service

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=UserLoginSchema)
async def login(body: UserLoginProcessSchema, auth_service: AuthService = Depends(get_auth_service)):
    """Ручка авторизации через имя и пароль"""
    try:
        return await auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserIncorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)


@router.get('/login/google', response_class=RedirectResponse)
async def google_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    """Ручка регистрации через google"""
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get('/google')
async def google_auth(auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str):
    """Ручка авторизации через google"""
    return await auth_service.google_auth(code=code)


@router.get('/login/yandex', response_class=RedirectResponse)
async def yandex_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    """Ручка регистрации через яндекс"""
    redirect_url = auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get('/yandex')
async def yandex_auth(auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str):
    """Ручка авторизации через яндекс"""
    return await auth_service.get_yandex_auth(code=code)
