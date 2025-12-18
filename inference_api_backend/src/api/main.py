from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.facts import router as facts_router
from src.api.routers.health import router as health_router
from src.config.settings import settings
from src.util.version import get_version

openapi_tags = [
    {"name": "facts", "description": "Fact retrieval and source listing"},
    {"name": "health", "description": "Health and liveness endpoints"},
]


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=get_version(settings.APP_VERSION),
        openapi_tags=openapi_tags,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    # Routers
    app.include_router(facts_router)
    app.include_router(health_router)

    # Root
    @app.get(
        "/",
        summary="API root",
        description="Minimal root endpoint. Visit /docs for interactive Swagger UI.",
        tags=["health"],
        responses={200: {"description": "Root message"}},
    )
    def root() -> dict:
        """Return minimal root message with pointer to Swagger docs."""
        return {
            "message": "Immortal Jellyfish Inference API",
            "docs": "/docs",
            "openapi": "/openapi.json",
        }

    return app


# FastAPI app instance
app = create_app()
