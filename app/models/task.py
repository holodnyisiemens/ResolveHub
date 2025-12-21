from enum import Enum as PyEnum
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Enum as SQLEnum, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.employee import Employee

class TaskStatus(PyEnum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    creator_email: Mapped[str] = mapped_column(String(255), nullable=False)

    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus, name="task_status"),
        nullable=False,
        default=TaskStatus.NEW,
        server_default=TaskStatus.NEW.value,
    )
    
    assignee_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("employees.id"), 
        nullable=True,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        server_default=func.now(),
        nullable=False,
    )

    assignee: Mapped[Optional["Employee"]] = relationship(
        "Employee",
        back_populates="tasks",
    )
