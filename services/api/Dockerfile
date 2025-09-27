# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS base
ARG ENV=prod
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PATH="/app/.venv/bin:$PATH"     APP_ENV=${ENV}

RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential && rm -rf /var/lib/apt/lists/* \
 && curl -LsSf https://astral.sh/uv/install.sh | sh \
 && mv /root/.local/bin/uv /usr/local/bin/uv \
 && chmod +x /usr/local/bin/uv


WORKDIR /app
# Workspace metadata first
COPY pyproject.toml ./
COPY packages/common/pyproject.toml packages/common/pyproject.toml
COPY services/api/pyproject.toml services/api/pyproject.toml

# Copy sources (workspace packages and this service)
COPY packages/common/artify_common packages/common/artify_common
COPY services/api/app services/api/app

# Now install deps (needs sources present for workspace)
RUN if [ "$APP_ENV" = "dev" ]; then uv sync --all-extras --dev; else uv sync --frozen; fi


RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["uv", "run", "artify-api"]
