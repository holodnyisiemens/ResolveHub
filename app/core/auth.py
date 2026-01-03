from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.auth import utils as auth_utils
from app.core.database import async_session_factory
from app.repositories.employee_repository import EmployeeRepository

security = HTTPBasic()


class AdminAuth(AuthenticationBackend):
    middlewares = []

    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    async def login(self, request: Request) -> bool:
        credentials: HTTPBasicCredentials = await request.form()
        username = credentials.get("username")
        password = credentials.get("password")
        async with async_session_factory() as session:
            repo = EmployeeRepository(session)
            employee = await repo.get_by_username(username)
            if employee and auth_utils.validate_password(
                password, employee.hashed_password
            ):
                request.session.update({"token": self.secret_key})
                return True
        return False

    async def logout(self, request: Request) -> None:
        request.session.clear()

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        return token == self.secret_key
