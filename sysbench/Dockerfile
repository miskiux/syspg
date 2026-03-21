FROM python:3.12-slim

RUN apt-get update && apt-get install -y sysbench postgresql-client && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

ENV VIRTUAL_ENV=/home/.venv
ENV PATH="/home/.venv/bin:$PATH"
ENV PYTHONPATH="/home/.venv/lib/python3.12/site-packages"

COPY . .