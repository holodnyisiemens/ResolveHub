from typing import TYPE_CHECKING

from sqlalchemy import Boolean, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.task import Task


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    hashed_password: Mapped[str] = mapped_column(LargeBinary, nullable=False)

    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="assignee",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"
