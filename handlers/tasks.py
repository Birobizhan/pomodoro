from fastapi import APIRouter, Depends, HTTPException

from exception import TaskNotFound
from service import TaskService
from schemas import Task, TaskCreateSchema
from repository import TaskRepository, CacheTask
from dependency import get_tasks_repository, get_cache_repository, get_task_service, get_request_user_id

router = APIRouter(prefix='/task', tags=['task'])
fixtures_tasks = []


@router.get('/all', response_model=list[Task])
async def get_tasks(task_service: TaskService = Depends(get_task_service), user_id: int = Depends(get_request_user_id)):
    return task_service.get_tasks(user_id=user_id)


@router.post('/')
async def create_task(body: TaskCreateSchema, task_service: TaskService = Depends(get_task_service),
                      user_id: int = Depends(get_request_user_id)):
    task = task_service.create_task(body, user_id)
    return task


@router.patch('/{task_id}')
async def update_task(task_id: int, name: str, task_service: TaskService = Depends(get_task_service),
                      user_id: int = Depends(get_request_user_id)):
    try:
        return task_service.update_name(task_id=task_id, name=name, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.delete('/{task_id', status_code=204)
async def delete_task(task_id: int, task_service: TaskService = Depends(get_task_service), user_id: int = Depends(get_request_user_id)):
    try:
        task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)