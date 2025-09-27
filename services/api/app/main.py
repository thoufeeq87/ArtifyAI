from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from artify_common import settings
from artify_common.logging import env_configure_from_vars

from .routes import router as v1_router
from .version import __version__

env_configure_from_vars()

app = FastAPI(
    title="ArtifyAIv.1 API",
    version=__version__,
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.app_env != "prod" else [],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api/v1")


def run() -> None:
    import uvicorn

    uvicorn.run(
        "services.api.app.main:app",
        host="0.0.0.0",
        port=settings.api_port,
        reload=(settings.app_env == "dev"),
        workers=1,
    )
