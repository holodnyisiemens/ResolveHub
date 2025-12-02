from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.task import TaskStatus


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )


class TaskAddDTO(BaseDTO):
    title: str
    description: str
    creator_email: EmailStr


class TaskDTO(TaskAddDTO):
    id: int
    status: TaskStatus
    assignee_id: int


class TaskUpdateDTO(BaseDTO):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None
