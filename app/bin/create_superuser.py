import asyncio
import sys

from app.core.database import async_session_factory
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeAddDTO
from app.services.employee_service import EmployeeService


async def create_superuser(username, password, email):
    async with async_session_factory() as session:
        repo = EmployeeRepository(session)
        service = EmployeeService(repo)
        superuser_data = EmployeeAddDTO(
            username=username,
            email=email,
            password=password,
            is_superuser=True,
        )
        await service.create(superuser_data)


async def main():
    if len(sys.argv) != 4:
        print(
            "Error. Use command like:\n"
            "python bin/create_superuser.py <username> <password> <email>"
        )
        sys.exit(1)

    username, password, email = sys.argv[1], sys.argv[2], sys.argv[3]
    await create_superuser(username, password, email)
    print(f"Created superuser: {username} ({email})")


if __name__ == "__main__":
    asyncio.run(main())
