# Dockerfile — ОФИЦИАЛЬНЫЙ и 100% рабочий способ с uv в Docker (2025)
FROM python:3.13-slim

# 1. Ставим только curl + системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app
COPY . .

# 4. Всё ставим глобально — быстро, надёжно, без .venv
RUN uv pip install --system --no-cache -e .[standard] && \
    uv pip install --system --no-cache alembic

# 5. Пользователь
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]