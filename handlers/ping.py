from fastapi import FastAPI, APIRouter
from settings import Settings

router = APIRouter(prefix='/ping', tags=['ping'])


@router.get('/')
async def ping():
    settings = Settings()

    return {'message': f'{settings.GOOGLE_TOKEN_ID}'}
