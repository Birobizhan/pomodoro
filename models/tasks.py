from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base


class Tasks(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    pomodoro_count: Mapped[int] = mapped_column()
    category_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey('UserProfile.id'), nullable=False)

    user: Mapped["UserProfile"] = relationship('UserProfile', back_populates='tasks')


class Categories(Base):
    __tablename__ = 'Categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
