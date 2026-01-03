from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.auth import utils as auth_utils
from app.core.config import settings
from app.di.deps import provide_employee_repository
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeDTO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.token_url)


async def validate_auth(
    username: str = Form(),
    password: str = Form(),
    employee_repo: EmployeeRepository = Depends(provide_employee_repository),
):
    user_not_exists_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"User {username} not found",
    )

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )

    inactive_exc = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"User {username} is inactive",
    )

    employee = await employee_repo.get_by_username(username)
    if not employee:
        raise user_not_exists_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=employee.hashed_password,
    ):
        raise unauthed_exc

    if not employee.is_active:
        raise inactive_exc

    return employee


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> EmployeeDTO:
    """Получение payload из токена"""
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    employee_repo: EmployeeRepository = Depends(provide_employee_repository),
) -> EmployeeDTO:
    """Получение аутентифицированного пользователя"""
    token_invalid_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Token invalid",
    )

    username: str | None = payload.get("sub")
    employee = await employee_repo.get_by_username(username)
    if not employee:
        raise token_invalid_exc

    return employee


async def get_current_active_auth_user(
    employee: EmployeeDTO = Depends(get_current_auth_user),
):
    """Получение аутентифицированного пользователя, если он активен"""
    if employee.is_active:
        return employee

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"User {employee.username} is inactive",
    )
