from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.models import Tasks, Categories
from app.tasks.schema import TaskCreateSchema


class TaskRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_tasks(self, user_id: int):
        async with self.db_session as session:
            tasks = (await session.execute(select(Tasks).where(Tasks.user_id == user_id))).scalars().all()
        return tasks

    async def get_task(self, task_id: int) -> Tasks | None:
        async with self.db_session as session:
            task: Tasks = (await session.execute(select(Tasks).where(Tasks.id == task_id))).scalar_one_or_none()
        return task

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        query = insert(Tasks).values(name=task.name, pomodoro_count=task.pomodoro_count, category_id=task.category_id, user_id=user_id).returning(Tasks.id)
        async with self.db_session as session:
            task_model = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return task_model

    async def update_name(self, task_id, name):
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        async with self.db_session as session:
            task = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return await self.get_task(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        async with self.db_session as session:
            await session.execute(delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id))
            await session.commit()

    async def get_task_by_category_name(self, category_name) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)
        async with self.db_session as session:
            task: list[Tasks] = (await session.execute(query)).scalars().all()
            return task

    async def get_user_task(self, task_id: int, user_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.db_session as session:
            task: Tasks = (await session.execute(query)).scalar_one_or_none()
        return task
