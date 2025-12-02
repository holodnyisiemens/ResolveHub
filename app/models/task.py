from enum import Enum as PyEnum

from sqlalchemy import Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TaskStatus(PyEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    title: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    creator_email: Mapped[str] = mapped_column(nullable=False)
    
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus),
        default=TaskStatus.NEW,
        nullable=False,
    )
    
    assignee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"), 
        nullable=True,
    )
