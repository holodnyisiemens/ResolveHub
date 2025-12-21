from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen

from pydantic import BaseModel, ConfigDict, EmailStr


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        str_strip_whitespace=True,
    )


class EmployeeAddDTO(BaseDTO):
    username: Annotated[str, MinLen(3), MaxLen(30)]
    email: Annotated[EmailStr, MaxLen(255)]
    password: Annotated[str, MinLen(6), MaxLen(128)]


class EmployeeDTO(BaseDTO):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool


class EmployeeUpdateDTO(BaseDTO):
    username: Optional[Annotated[str, MinLen(3), MaxLen(30)]] = None
    email: Optional[Annotated[EmailStr, MaxLen(255)]] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class EmployeeChangePasswordDTO(BaseDTO):
    current_password: str
    new_password: Annotated[str, MinLen(6), MaxLen(128)]
