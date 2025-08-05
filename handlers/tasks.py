from fastapi import APIRouter, Depends

from service import TaskService
from shemas.tasks import Task
from repository import TaskRepository, CacheTask
from dependency import get_tasks_repository, get_cache_repository, get_task_service

router = APIRouter(prefix='/task', tags=['task'])
fixtures_tasks = []


@router.get('/all', response_model=list[Task])
async def get_tasks(task_service: TaskService = Depends(get_task_service)):
    return task_service.get_tasks()


@router.post('/')
async def create_task(data: Task, task_repository: TaskRepository = Depends(get_tasks_repository)):
    task_repository.create_task(data)
    return {'text': 'Create task'}


@router.patch('/{task_id}')
async def update_task(task_id: int, name: str, task_repository: TaskRepository = Depends(get_tasks_repository)):
    return task_repository.update_name(task_id, name)


@router.delete('/{task_id', status_code=204)
async def delete_task(task_id: int, task_repository: TaskRepository = Depends(get_tasks_repository)):
    task_repository.delete_task(task_id)
