FROM python:3.11-slim

RUN apt-get update && apt-get install -y sysbench postgresql-client && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /sysbench
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

ENV VIRTUAL_ENV=/sysbench/.venv
ENV PATH="/sysbench/.venv/bin:$PATH"

COPY . .

CMD ["python3", "/sysbench/runner.py"]