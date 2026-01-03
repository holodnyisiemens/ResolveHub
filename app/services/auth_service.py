from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pydantic import ValidationError

from app.auth import utils as auth_utils
from app.core.config import settings
from app.di.deps import provide_employee_repository
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.auth import TokenData
from app.schemas.employee import EmployeeDTO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.token_url)


async def validate_auth(
    username: str = Form(),
    password: str = Form(),
    employee_repo: EmployeeRepository = Depends(provide_employee_repository),
) -> EmployeeDTO:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )

    inactive_exc = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive",
    )

    employee = await employee_repo.get_by_username(username)
    if not employee:
        raise unauthed_exc

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
) -> TokenData:
    """Получение payload из токена"""
    try:
        payload = auth_utils.decode_jwt(token=token)
        return TokenData(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error",
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )


async def get_current_auth_user(
    payload: TokenData = Depends(get_current_token_payload),
    employee_repo: EmployeeRepository = Depends(provide_employee_repository),
) -> EmployeeDTO:
    """Получение аутентифицированного пользователя"""
    token_invalid_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid",
    )

    username = payload.sub
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
        detail="User inactive",
    )
