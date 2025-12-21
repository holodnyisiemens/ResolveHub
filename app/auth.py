from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
from app.repositories.employee_repository import EmployeeRepository
from app.core.database import async_session_factory
from app.core.security import verify_password

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
            if employee and verify_password(password, employee.hashed_password):
                # Можно проверить secret_key для токена сессии или пропустить
                request.session.update({"token": self.secret_key})
                return True
        return False

    async def logout(self, request: Request) -> None:
        request.session.clear()

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        return token == self.secret_key
