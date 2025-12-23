FROM python:3.12.6-slim

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir poetry==2.2.1

COPY pyproject.toml poetry.lock ./

# Configure Poetry and install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-cache --no-root --no-interaction --no-ansi
    
# Migrations files
COPY alembic.ini ./
COPY migrations ./migrations
    
COPY app ./app

COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
CMD ["python", "-m", "app.main"]
