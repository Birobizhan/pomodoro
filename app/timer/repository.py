from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.models import Tasks, TaskStatus


class TimerRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_task(self, task_id: int, user_id: int) -> Tasks:
        """Получение задачи"""
        async with self.db_session as session:
            query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
            task = (await session.execute(query)).scalar_one_or_none()
        return task

    async def change_status_in_progress(self, task_id: int) -> None:
        """Изменение статуса задачи на: В процессе"""
        async with self.db_session as session:
            query = update(Tasks).where(Tasks.id == task_id).values(status=TaskStatus.IN_PROGRESS)
            await session.execute(query)
            await session.commit()

    async def change_status_completed(self, task_id: int) -> None:
        """Изменение статуса задачи на: Завершена"""
        async with self.db_session as session:
            query = update(Tasks).where(Tasks.id == task_id).values(status=TaskStatus.COMPLETED)
            await session.execute(query)
            await session.commit()

    async def change_status_planned(self, task_id: int) -> None:
        """Изменение статуса задачи на: В планах"""
        async with self.db_session as session:
            query = update(Tasks).where(Tasks.id == task_id).values(status=TaskStatus.PLANNED)
            await session.execute(query)
            await session.commit()
