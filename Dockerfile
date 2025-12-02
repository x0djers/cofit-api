FROM python:3.13-slim

ADD https://astral.sh/uv/install.sh /install-uv.sh
RUN sh /install-uv.sh && rm /install-uv.sh
ENV PATH="/root/.cargo/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-cache

COPY . .

RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser /app
USER appuser

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
