from fastapi import APIRouter

from src.domain.models import FactResponse, ErrorResponse

from src.services.fact_service import get_immortal_jellyfish_fact

router = APIRouter(prefix="/facts")


@router.get(
    "/immortal-jellyfish",
    response_model=FactResponse,
    summary="Get immortal jellyfish fact",
    description=(
        "Returns a curated fact about the 'immortal jellyfish' (Turritopsis dohrnii), "
        "including links to reputable sources that both support and contextualize/refute aspects of the claim."
    ),
    responses={
        200: {
            "description": "Fact response with supporting and refuting sources",
            "content": {
                "application/json": {
                    "example": {
                        "fact": "Turritopsis dohrnii can revert its mature medusa stage back to a juvenile polyp stage, allowing it to sidestep death under certain conditions.",
                        "supporting_sources": [
                            {
                                "title": "Turritopsis dohrnii: the 'immortal jellyfish'",
                                "url": "https://www.nationalgeographic.com/animals/article/immortal-jellyfish",
                                "note": "Popular science article describing the life cycle reversal.",
                            },
                            {
                                "title": "Reversing the life cycle: medusae reverting to polyps in Turritopsis",
                                "url": "https://link.springer.com/article/10.1007/BF02391156",
                                "note": "Peer‑reviewed study documenting reversal.",
                            },
                        ],
                        "refuting_sources": [
                            {
                                "title": "The myth of true biological immortality",
                                "url": "https://www.science.org/content/article/no-such-thing-immortal-jellyfish",
                                "note": "Explains limitations and misuse of 'immortal' term.",
                            },
                            {
                                "title": "Contextualizing 'immortality' in Turritopsis dohrnii",
                                "url": "https://www.nature.com/scitable/blog/science-sushi/immortal_jellyfish_immortalized_in_myth/",
                                "note": "Clarifies that mortality from predation/disease still applies.",
                            },
                        ],
                    }
                }
            },
        },
        500: {
            "description": "Internal error",
            "model": ErrorResponse,
        },
    },
)
# PUBLIC_INTERFACE
def get_immortal_jellyfish() -> FactResponse:
    """Return the immortal jellyfish fact and curated sources."""
    return get_immortal_jellyfish_fact()
