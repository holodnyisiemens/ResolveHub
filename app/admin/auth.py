from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.auth import utils as auth_utils
from app.core.database import async_session_factory
from app.repositories.employee_repository import EmployeeRepository


class AdminAuth(AuthenticationBackend):
    """Session-based authentication backend for sqladmin."""

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username: str | None = form.get("username")
        password: str | None = form.get("password")

        if not username or not password:
            return False

        async with async_session_factory() as session:
            repo = EmployeeRepository(session)
            employee = await repo.get_by_username(username)

            if (
                employee
                and employee.is_active
                and auth_utils.validate_password(password, employee.hashed_password)
            ):
                # сохраняем пользователя в сессии
                request.session["admin_user"] = employee.username
                return True

        return False

    async def logout(self, request: Request) -> None:
        request.session.clear()

    async def authenticate(self, request: Request) -> bool:
        """Called on every admin request."""
        return "admin_user" in request.session
