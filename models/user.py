from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship



class UserProfile(Base):
    __tablename__ = 'UserProfile'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    tasks: Mapped[list["Tasks"]] = relationship('Tasks', back_populates='user')
