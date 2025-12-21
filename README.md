# ResolveHub

ResolveHub - трекер задач, создаваемых по Email.

## Запуск проекта

### Windows

Активируем виртуальное окружение:
```
.venv\Scripts\activate
```

Старт приложения:
```
python -m app.main
```

## Использование

Создание суперюзера:
```
python bin/create_superuser.py <username> <password> <email>
```

Например:
```
python bin/create_superuser.py admin 123456 example@gmail.com
```

Все задачи:
http://localhost:8000/tasks/

Страница админа:
http://localhost:8000/admin/task/list
