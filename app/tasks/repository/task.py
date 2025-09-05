from sqlalchemy import select, delete, update, insert
from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.models import Tasks, TaskStatus
from app.tasks.schema import TaskCreateSchema


class TaskRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_tasks(self, user_id: int) -> Sequence[Tasks]:
        """Метод для получения всех задач пользователя из бд"""
        async with self.db_session as session:
            tasks: Sequence[Tasks] = (await session.execute(select(Tasks).where(Tasks.user_id == user_id))).scalars().all()
        return tasks

    async def get_task(self, task_id: int) -> Tasks:
        """Метод получения одной задачи из бд"""
        async with self.db_session as session:
            task: Tasks = (await session.execute(select(Tasks).where(Tasks.id == task_id))).scalar_one_or_none()
        return task

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int | None:
        """Метод создания новой задачи"""
        query = insert(Tasks).values(name=task.name, pomodoro_count=task.pomodoro_count, user_id=user_id, status=TaskStatus.PLANNED).returning(Tasks.id)
        async with self.db_session as session:
            task_model: int | None = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
        return task_model

    async def update_name(self, task_id: int, name: str) -> Tasks:
        """Метод обновления названия задачи"""
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        async with self.db_session as session:
            task = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            answer = await self.get_task(task)
        return answer

    async def delete_task(self, task_id: int, user_id: int) -> None:
        """Метод удаления задачи"""
        async with self.db_session as session:
            await session.execute(delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id))
            await session.commit()

    async def get_user_task(self, task_id: int, user_id: int) -> Tasks | None:
        """Метод получения одной задачи с проверкой, что она принадлежит нужному пользователю"""
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.db_session as session:
            task: Tasks = (await session.execute(query)).scalar_one_or_none()
        return task
