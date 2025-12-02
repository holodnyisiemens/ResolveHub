import asyncio
from app.core.database import async_session_factory
from app.models.employee import Employee
from app.core.security import get_password_hash  # Ваша функция для хэширования пароля
import sqlalchemy
from app.core.config import settings

TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD.get_secret_value()}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/test_resolvehub"
)
async def create_superuser(username: str, password: str):
    async with async_session_factory() as session:
        # Проверяем, существует ли пользователь
        result = await session.execute(
            # импорт select на верхнем уровне
            
            sqlalchemy.select(Employee).where(Employee.username == username)
        )
        user = result.scalars().first()
        
        if user:
            # Обновляем существующего пользователя, делаем суперюзером
            user.is_superuser = True
            user.hashed_password = get_password_hash(password)
            print(f"Пользователь {username} обновлен до суперпользователя.")
        else:
            # Создаем нового суперпользователя
            user = Employee(
                username=username,
                hashed_password=get_password_hash(password),
                is_superuser=True
            )
            session.add(user)
            print(f"Суперпользователь {username} создан.")

        await session.commit()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Использование: python create_superuser.py <username> <password>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    asyncio.run(create_superuser(username, password))
