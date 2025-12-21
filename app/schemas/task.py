from typing import Optional, Annotated
from annotated_types import MaxLen
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.task import TaskStatus


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        str_strip_whitespace=True,
    )


class TaskAddDTO(BaseDTO):
    title: Optional[Annotated[str, MaxLen(255)]] = None
    description: Optional[Annotated[str, MaxLen(2000)]] = None
    creator_email: Annotated[EmailStr, MaxLen(255)]


class TaskDTO(TaskAddDTO):
    id: int
    status: TaskStatus
    assignee_id: Optional[int]
    created_at: datetime


class TaskUpdateDTO(BaseDTO):
    title: Optional[Annotated[str, MaxLen(255)]] = None
    description: Optional[Annotated[str, MaxLen(2000)]] = None
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None
