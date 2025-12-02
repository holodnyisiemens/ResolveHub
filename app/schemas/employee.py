from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen

from pydantic import BaseModel, ConfigDict, EmailStr


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )


class EmployeeAddDTO(BaseDTO):
    username: Annotated[str, MinLen(2), MaxLen(30)]
    email: EmailStr


class EmployeeDTO(EmployeeAddDTO):
    id: int
    is_active: bool


class EmployeeUpdateDTO(BaseDTO):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
