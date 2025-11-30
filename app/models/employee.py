from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[EmailStr]
    is_active: Mapped[bool]
