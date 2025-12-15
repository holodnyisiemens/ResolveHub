#!/usr/bin/env python3
import sys
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.core.database import sync_engine
from app.core.security import get_password_hash as hash_password
from app.models.employee import Employee

SessionLocal = sessionmaker(bind=sync_engine)

def create_superuser(username: str, password: str):
    session = SessionLocal()
    try:
        result = session.execute(
            select(Employee).where(Employee.username == username)
        )
        user = result.scalar_one_or_none()
        
        if user:
            user.is_superuser = True
            user.hashed_password = hash_password(password)
            print(f"Пользователь {username} обновлён")
        else:
            user = Employee(
                username=username,
                hashed_password=hash_password(password),
                is_superuser=True,
                email=f"{username}@example.com"
            )
            session.add(user)
            print(f"Суперпользователь {username} создан")
        
        session.commit()
        print(f"Логин: {username}, Пароль: {password}")
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("python create_superuser.py <username> <password>")
        sys.exit(1)
    
    username, password = sys.argv[1], sys.argv[2]
    create_superuser(username, password) 
