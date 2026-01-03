from typing import Optional

from pydantic import BaseModel


class TokenInfo(BaseModel):
    """Схема для JWT токена"""

    access_token: str
    token_type: str


# class TokenData(BaseModel):
#     """Данные, которые хранятся в JWT токене (payload)"""
#     username: Optional[str] = None
#     user_id: Optional[int] = None


# class UserLogin(BaseModel):
#     """Схема для входа пользователя"""
#     username: str
#     password: str
