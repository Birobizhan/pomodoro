from app.infrastructure.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.tasks.models import Tasks


class UserProfile(Base):
    __tablename__ = 'UserProfile'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    google_access_token: Mapped[str | None] = mapped_column()
    yandex_access_token: Mapped[str | None] = mapped_column()
    email: Mapped[str | None] = mapped_column()
    name: Mapped[str | None] = mapped_column()
    tasks: Mapped[list["Tasks"]] = relationship('Tasks', back_populates='user')
