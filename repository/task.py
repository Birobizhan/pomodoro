from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from models import Tasks, Categories
from schemas import TaskCreateSchema
from database import get_db_session


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self, user_id: int):
        with self.db_session() as session:
            tasks = session.execute(select(Tasks).where(Tasks.user_id == user_id)).scalars().all()
        return tasks

    def get_task(self, task_id: int) -> Tasks | None:
        with self.db_session() as session:
            task: Tasks = session.execute(select(Tasks).where(Tasks.id == task_id)).scalar_one_or_none()
        return task

    def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_model = Tasks(name=task.name, pomodoro_count=task.pomodoro_count, category_id=task.category_id, user_id=user_id)
        with self.db_session() as session:
            session.add(task_model)
            session.commit()
            return task_model.id

    def update_name(self, task_id, name):
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        with self.db_session() as session:
            task = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_task(task)

    def delete_task(self, task_id: int, user_id: int) -> None:
        with self.db_session() as session:
            session.execute(delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id))
            session.commit()

    def get_task_by_category_name(self, category_name) -> list[Tasks]:
        query = select(Tasks).join(Categories,Tasks.category_id == Categories.id).where(Categories.name == category_name)
        with self.db_session() as session:
            task: list[Tasks] = session.execute(query).scalars().all()
            return task

    def get_user_task(self, task_id: int, user_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        with self.db_session() as session:
            task: Tasks = session.execute(query).scalar_one_or_none()
        return task

def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)
