from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class TaskStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class BaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TaskAddDTO(BaseDTO):
    title: str
    description: str
    creator_email: EmailStr


class TaskDTO(TaskAddDTO):
    id: int
    status: TaskStatus
    assignee_id: int


class TaskUpdateDTO(BaseDTO):
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus]
    assignee_id: Optional[int]

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )
