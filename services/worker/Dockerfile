# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS base
ARG ENV=prod
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PATH="/app/.venv/bin:$PATH"     APP_ENV=${ENV}

RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential && rm -rf /var/lib/apt/lists/* \
 && curl -LsSf https://astral.sh/uv/install.sh | sh \
 && mv /root/.local/bin/uv /usr/local/bin/uv \
 && chmod +x /usr/local/bin/uv


WORKDIR /app
COPY pyproject.toml ./
COPY packages/common/pyproject.toml packages/common/pyproject.toml
COPY services/worker/pyproject.toml services/worker/pyproject.toml

# Copy sources first
COPY packages/common/artify_common packages/common/artify_common
COPY services/worker/worker services/worker/worker

# Then uv sync
RUN if [ "$APP_ENV" = "dev" ]; then uv sync --all-extras --dev; else uv sync --frozen; fi


RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["uv", "run", "artify-worker"]
