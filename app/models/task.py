from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from schemas.task import TaskStatus


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    creator_email: Mapped[EmailStr]
    status: Mapped[TaskStatus]
    assignee_id: Mapped[int]
