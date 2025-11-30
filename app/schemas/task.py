from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr


class TaskStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class DTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TaskAddDTO(DTO):
    title: str
    description: str
    creator_email: EmailStr


class TaskDTO(TaskAddDTO):
    id: int
    status: TaskStatus
