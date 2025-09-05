from fastapi import APIRouter

router = APIRouter(prefix='/ping', tags=['ping'])


@router.get('/{message}')
async def ping(message: str):
    """Ручка для проверки работоспособности api"""
    return {'message': f'ping {message}'}
