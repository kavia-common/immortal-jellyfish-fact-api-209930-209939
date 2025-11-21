from fastapi import APIRouter

from .facts import router as facts_router

# Single API router to aggregate all versioned routes
api_router = APIRouter()
api_router.include_router(facts_router, tags=["facts"])
