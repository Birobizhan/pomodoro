from fastapi import APIRouter, Depends, HTTPException
from app.exception import TaskNotFound
from app.tasks.service import TaskService
from app.tasks.schema import Task, TaskCreateSchema
from app.dependency import get_task_service, get_request_user_id

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.get('/all', response_model=list[Task])
async def get_tasks(task_service: TaskService = Depends(get_task_service), user_id: int = Depends(get_request_user_id)):
    """Ручка для получения всех задач пользователя"""
    tasks = await task_service.get_tasks(user_id=user_id)
    return tasks


@router.get('/{task_id}')
async def get_task_by_id(task_id: int, task_service: TaskService = Depends(get_task_service),
                         user_id: int = Depends(get_request_user_id)):
    """Ручка для получения конкретной задачи по id"""
    task = await task_service.get_task_by_id(task_id=task_id, user_id=user_id)
    return task


@router.post('/')
async def create_task(body: TaskCreateSchema, task_service: TaskService = Depends(get_task_service),
                      user_id: int = Depends(get_request_user_id)):
    """Ручка создания задачи"""
    task = await task_service.create_task(body, user_id)
    return task


@router.patch('/{task_id}')
async def update_task(task_id: int, name: str, task_service: TaskService = Depends(get_task_service),
                      user_id: int = Depends(get_request_user_id)):
    """Ручка обновления имени задачи"""
    try:
        return await task_service.update_name(task_id=task_id, name=name, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.delete('/{task_id}', status_code=204)
async def delete_task(task_id: int, task_service: TaskService = Depends(get_task_service), user_id: int = Depends(get_request_user_id)):
    """Ручка удаления задачи из бд"""
    try:
        await task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
