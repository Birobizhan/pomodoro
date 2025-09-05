from dataclasses import dataclass
from fastapi import HTTPException
from app.tasks.schema import Task
from app.timer.repository import TimerRepository


@dataclass
class TimerService:
    timer_repository: TimerRepository

    async def get_task_by_id(self, task_id: int, user_id: int) -> Task:
        task = await self.timer_repository.get_task(task_id=task_id, user_id=user_id)
        if task:
            return Task.model_validate(task)
        raise HTTPException(status_code=404, detail='Задачи с таким id не существует')

    async def check_permission(self, task_id: int, user_id: int) -> bool:
        """Проверка прав пользователя"""
        task = await self.timer_repository.get_task(task_id=task_id, user_id=user_id)
        if task:
            return True
        return False

    async def change_status_in_progress(self, task_id: int):
        """Смена статуса задачи на: В процессе"""
        await self.timer_repository.change_status_in_progress(task_id=task_id)

    async def change_status_planned(self, task_id: int):
        """Смена статуса задачи на: В планах"""
        await self.timer_repository.change_status_planned(task_id=task_id)

    async def change_status_completed(self, task_id: int):
        """Смена статуса задачи на: Завершена"""
        await self.timer_repository.change_status_completed(task_id=task_id)
