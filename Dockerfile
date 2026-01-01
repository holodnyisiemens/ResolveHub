FROM python:3.12.6-slim

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir poetry==2.2.1

COPY pyproject.toml poetry.lock /app/

# Configure Poetry and install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-cache --no-root --no-interaction --no-ansi
    
# Migrations files
COPY alembic.ini /app/alembic.ini
COPY migrations /app/migrations
    
COPY app /app/app/

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY certs /app/certs

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
CMD ["python", "-m", "app.main"]
