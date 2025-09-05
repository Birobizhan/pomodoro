from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.infrastructure.database import Base
from sqlalchemy.dialects import postgresql
import enum


class TaskStatus(enum.Enum):
    PLANNED = "В планах"
    IN_PROGRESS = "В процессе"
    COMPLETED = "Завершена"

    def __str__(self):
        return self.value


class Tasks(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    pomodoro_count: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('UserProfile.id'), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(postgresql.ENUM(TaskStatus, name='status', create_type=False), default=TaskStatus.PLANNED, nullable=False)
    user: Mapped["UserProfile"] = relationship('UserProfile', back_populates='tasks')
