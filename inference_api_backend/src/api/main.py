from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import api_router
from src.core.config import get_cors_settings
from src.core.version import get_version

# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """Create and configure the FastAPI application with metadata, CORS, and routes."""
    app = FastAPI(
        title="Immortal Jellyfish Fact API",
        description=(
            "An API that returns a curated fact about the 'immortal jellyfish' (Turritopsis dohrnii), "
            "including supporting and refuting sources."
        ),
        version=get_version(),
        openapi_tags=[
            {"name": "health", "description": "Service health and liveness endpoints."},
            {"name": "facts", "description": "Fact retrieval endpoints."},
        ],
    )

    # Configure CORS
    cors_cfg = get_cors_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_cfg["allow_origins"],
        allow_credentials=cors_cfg["allow_credentials"],
        allow_methods=cors_cfg["allow_methods"],
        allow_headers=cors_cfg["allow_headers"],
    )

    # Health endpoints
    @app.get(
        "/",
        tags=["health"],
        summary="Liveness probe",
        response_model=dict,
        responses={200: {"description": "Service is alive"}},
    )
    def root():
        # Return HealthResponse shape but inline dict to avoid circular import at startup
        return {"status": "ok"}

    @app.get(
        "/health",
        tags=["health"],
        summary="Health check",
        response_model=dict,
        responses={200: {"description": "Service is healthy"}},
    )
    def health():
        return {"status": "ok"}

    # Mount API router under /v1
    app.include_router(api_router, prefix="/v1")

    return app


# Instance used by ASGI servers and OpenAPI generation
app = create_app()
