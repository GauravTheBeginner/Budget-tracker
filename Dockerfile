# Python 3.10 on Debian 12 (bookworm). Pinned so the base OS doesn't change underneath us.
FROM python:3.10-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Only what the project actually needs: psql for debugging the DB, cron for scheduling, tzdata for dates.
# All Python deps (psycopg2-binary, pandas, numpy, ...) ship prebuilt wheels, so no compilers are required.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    tzdata \
    cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies first so this layer is cached between code changes
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN mkdir -p /app/logs

# Environment variables come from .env via `env_file` in docker-compose.yml at runtime.
