# ArtifyAIv.1

Dockerized monorepo with FastAPI (api), Celery worker + Beat (worker/scheduler), Redis, Flower, CI/CD, and code quality tools.

## Quick start

```bash
cp .env.example .env
# set GHCR_OWNER in .env
make up
```

- API: http://localhost:8000/api/v1/health
- Docs: http://localhost:8000/api/v1/docs
- Flower: http://localhost:5555
