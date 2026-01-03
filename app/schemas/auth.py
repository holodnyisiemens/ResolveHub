from datetime import datetime

from pydantic import BaseModel, EmailStr


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str
    username: str
    email: EmailStr
    exp: int
    iat: int


class MeResponse(BaseModel):
    username: str
    email: EmailStr
    logged_in_at: datetime
