from typing import Annotated
from annotated_types import MaxLen, MinLen

from pydantic import BaseModel, ConfigDict, EmailStr


class DTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class EmployeeAddDTO(DTO):
    username: Annotated[str, MinLen(2), MaxLen(30)]
    email: EmailStr


class EmployeeDTO(EmployeeAddDTO):
    id: int
    is_active: bool
