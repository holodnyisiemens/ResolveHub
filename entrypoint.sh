#!/bin/bash

set -e

# применение миграций
alembic upgrade head

# запуск приложения
exec "$@"
