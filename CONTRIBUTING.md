# Contributing to ArtifyAIv.1

## Local Dev
- Install [uv](https://astral.sh/uv): `curl -LsSf https://astral.sh/uv/install.sh | sh` (or PowerShell variant).
- `make uv-setup`
- `cp .env.example .env`
- `make up` (Docker Compose)

## Checks
- `make format` before committing.
- `make lint && make test` must pass (80% coverage).

## Commit & PR
- Use conventional-ish messages.
- Create PRs to `main`. CI runs on `main` and `feature/*`.
