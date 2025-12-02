from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.repositories.employee_repository import EmployeeRepository
from app.core.database import async_session
from app.core.security import verify_password
security = HTTPBasic()

async def get_current_employee(credentials: HTTPBasicCredentials = Depends(security)):
    async with async_session() as session:
        repo = EmployeeRepository(session)
        employee = await repo.get_by_username(credentials.username)  # Добавьте этот метод в репозиторий
        if not employee or not verify_password(credentials.password, employee.hashed_password):  # Реализуйте verify_password
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return employee
