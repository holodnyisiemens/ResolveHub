Если python ругается, то использовать
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Подключение скрипта
.venv\Scripts\activate

Для запуска сервера
uvicorn app.main:app --reload

Для создания суперюзера
python create_superuser.py admin mypassword

Просмотр всех заданий
http://localhost:8000/tasks/

Просмотр страницы админа
http://127.0.0.1:8000/admin/task/list

Логин admin

Пароль mypassword

