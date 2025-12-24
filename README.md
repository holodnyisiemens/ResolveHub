# ResolveHub

ResolveHub - трекер задач, создаваемых по Email.

## Запуск проекта через Docker

1. Клонируем проект:
```
git clone https://github.com/holodnyisiemens/ResolveHub.git
```

2. Переходим в рабочую директорию
```
cd ResolveHub
```

3. ВАЖНО! На основе .env.template создаем файл .env и указываем необходимые настройки:

`DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME` - настройка БД PostgreSQL (см. docker-compose.yaml)

`SECRET_KEY` - секретный ключ для авторизации в админ-панели

`SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD` - настройки работы для отправки писем по протоколу SMTP

`IMAP_HOST, IMAP_PORT, IMAP_USER, IMAP_PASSWORD` - настройки работы для получения писем по протоколу IMAP

`EMAIL_FOR_TESTS` - email адрес получателя для тестовых сообщений

`API_URL` - адрес для работы с API

4. Запускаем проект:
```
docker compose up -d
```

5. Список контейнеров:
```
docker ps
```

## Использование

### Админ-панель

Шаблон команды создания суперюзера (админа):
```
docker exec resolvehub python -m app.bin.create_superuser <username> <password> <email>
```

Например:
```
docker exec resolvehub python -m app.bin.create_superuser admin 123456 example@gmail.com
```

Админ-панель: http://localhost:8000/admin/

На админ-панели можно создавать задачи и других пользователей, которым можно будет назначать задачи

### Задачи

Страница задач: http://localhost:8000/tasks/

При отправлении письма по email, который указывается в .env как IMAP_USER, будет создана задача на странице задач

Ответные письма будут отправлены с email, который указывается как SMTP_USER

### API

Работа напрямую с API через интерактивную документацию: http://localhost:8000/docs/

## Дополнительно

Тестирование отправки email по адресу, указанному в .env как EMAIL_FOR_TESTS:
```
docker exec resolvehub python -um app.bin.send_test_email
```

Тестирование приема email (если основное приложение уже запущено принятые письма будут добавляться в список задач):
```
docker exec resolvehub python -um app.bin.email_process_test_worker
```

Запуск всех тестов pytest (из корневой директории):
```
pytest
```
