from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.auth import utils as auth_utils
from app.core.config import settings
from app.schemas.auth import MeResponse, TokenData, TokenInfo
from app.schemas.employee import EmployeeDTO
from app.services.auth_service import (
    get_current_active_auth_user,
    get_current_token_payload,
    validate_auth,
)

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=TokenInfo)
async def auth_jwt_login(
    user: EmployeeDTO = Depends(validate_auth),
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }

    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type=settings.auth_jwt.token_type,
    )


@router.get("/me", response_model=MeResponse)
async def auth_jwt_me(
    employee: EmployeeDTO = Depends(get_current_active_auth_user),
    payload: TokenData = Depends(get_current_token_payload),
):
    """Проверка аутентификации текущего пользователя"""
    logged_in_at = datetime.fromtimestamp(payload.iat, tz=timezone.utc)
    return MeResponse(
        username=employee.username,
        email=employee.email,
        logged_in_at=logged_in_at,
    )
