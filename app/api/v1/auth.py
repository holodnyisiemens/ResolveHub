from fastapi import APIRouter, Depends

from app.auth import utils as auth_utils
from app.schemas.auth import TokenInfo
from app.schemas.employee import EmployeeDTO
from app.services.auth_service import (
    get_current_active_auth_user,
    get_current_token_payload,
    validate_auth,
)

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=TokenInfo)
async def auth_jwt(
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
        token_type="Bearer",
    )


@router.get("/me")
async def auth_jwt_check_self(
    employee: EmployeeDTO = Depends(get_current_active_auth_user),
    payload: dict = Depends(get_current_token_payload),
):
    """Проверка аутентификации текущего пользователя"""
    iat = payload.get("iat")
    return {
        "username": employee.username,
        "email": employee.email,
        "logged_in_at": iat,
    }
