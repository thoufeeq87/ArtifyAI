# Variables
ENV ?= dev
VERSION ?= 0.1.0
IMAGE_BASE ?= $(IMAGE_BASE)
API_IMAGE := $(IMAGE_BASE)-api
WORKER_IMAGE := $(IMAGE_BASE)-worker
SCHED_IMAGE := $(IMAGE_BASE)-scheduler

export UV_SYSTEM_PYTHON=0

.PHONY: help
help:
	@echo "Common targets:"
	@echo "  uv-setup        Create venv & install deps (workspace dev)"
	@echo "  lint            Run ruff & black --check & mypy"
	@echo "  format          Run black & ruff --fix"
	@echo "  test            Run pytest with coverage"
	@echo "  up              docker compose up (dev)"
	@echo "  down            docker compose down -v"
	@echo "  build-images    Build api/worker/scheduler images (prod)"
	@echo "  push-images     Push images to GHCR (requires login)"

.PHONY: uv-setup
uv-setup:
	@which uv >/dev/null || (curl -LsSf https://astral.sh/uv/install.sh | sh)
	uv sync --all-extras --dev

.PHONY: lint
lint:
	uv run ruff check .
	uv run black --check .
	uv run mypy services packages

.PHONY: format
format:
	uv run black .
	uv run ruff check . --fix

.PHONY: test
test:
	REDIS_URL="redis://localhost:6379/0" CELERY_BROKER_URL="redis://localhost:6379/0" CELERY_RESULT_BACKEND="redis://localhost:6379/1" uv run pytest

.PHONY: up
up:
	docker compose --profile dev up --build

.PHONY: down
down:
	docker compose down -v

.PHONY: build-images
build-images:
	docker build -t $(API_IMAGE):$(VERSION) -f services/api/Dockerfile --build-arg ENV=prod .
	docker build -t $(WORKER_IMAGE):$(VERSION) -f services/worker/Dockerfile --build-arg ENV=prod .
	docker build -t $(SCHED_IMAGE):$(VERSION) -f services/scheduler/Dockerfile --build-arg ENV=prod .

.PHONY: push-images
push-images:
	docker push $(API_IMAGE):$(VERSION)
	docker push $(WORKER_IMAGE):$(VERSION)
	docker push $(SCHED_IMAGE):$(VERSION)
