from fastapi import APIRouter
from src.core.schemas import FactResponse, SourceLink
from src.core.service import JellyfishFactService

router = APIRouter(prefix="/v1", tags=["facts"])

_service = JellyfishFactService()


# PUBLIC_INTERFACE
@router.get(
    "/fact",
    response_model=FactResponse,
    summary="Get curated fact about the 'immortal jellyfish'",
    description="Returns a curated fact about Turritopsis dohrnii with supporting and refuting sources.",
    responses={
        200: {"description": "Fact payload returned successfully"},
    },
)
def get_fact() -> FactResponse:
    """Return a curated fact about the 'immortal jellyfish' and source links."""
    return _service.get_fact()


# PUBLIC_INTERFACE
@router.get(
    "/sources",
    response_model=dict,
    summary="Get source links only",
    description="Returns supporting and refuting sources as separate arrays.",
    responses={
        200: {
            "description": "Sources returned successfully",
            "content": {
                "application/json": {
                    "example": {
                        "supports": [SourceLink.model_validate(SourceLink.model_config["json_schema_extra"]["example"]).model_dump()],
                        "refutes": [SourceLink.model_validate(SourceLink.model_config["json_schema_extra"]["example"]).model_dump()],
                    }
                }
            },
        }
    },
)
def get_sources() -> dict:
    """Return only the lists of supporting and refuting sources."""
    supports, refutes = _service.get_sources()
    return {"supports": supports, "refutes": refutes}
