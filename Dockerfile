FROM python:3.12-slim

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH="$POETRY_HOME/bin:$PATH"

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./


RUN poetry install --no-root


COPY . .

# Запускаем приложение
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
