from fastapi import APIRouter

router = APIRouter(tags=["health"])


# PUBLIC_INTERFACE
@router.get(
    "/health",
    summary="Health check",
    description="Returns a simple health status for liveness checks.",
    responses={200: {"description": "Service is healthy"}},
)
def health() -> dict:
    """Health endpoint used for liveness and readiness checks.

    Returns:
        dict: A simple status object.
    """
    return {"status": "ok"}
