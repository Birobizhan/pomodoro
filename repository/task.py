from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from database import Tasks, get_db_session, Categories
from shemas.tasks import Task


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self):
        with self.db_session() as session:
            task = session.execute(select(Tasks)).scalars().all()
        return task

    def get_task(self, task_id: int) -> Tasks | None:
        with self.db_session() as session:
            task = session.execute(select(Tasks).where(Tasks.id == task_id)).scalar_one_or_none()
        return task

    def create_task(self, task: Task) -> None:
        task_model = Tasks(name=task.name, pomodoro_count=task.pomodoro_count, category_id=task.category_id)
        with self.db_session() as session:
            session.add(task_model)
            session.commit()

    def update_name(self, task_id, name):
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        with self.db_session() as session:
            task = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_task(task)

    def delete_task(self, task_id: int) -> None:
        with self.db_session() as session:
            session.execute(delete(Tasks).where(Tasks.id == task_id))
            session.commit()

    def get_task_by_category_name(self, category_name) -> list[Tasks]:
        query = select(Tasks).join(Categories,Tasks.category_id == Categories.id).where(Categories.name == category_name)
        with self.db_session() as session:
            task: list[Tasks] = session.execute(query).scalars().all()
            return task

def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)
