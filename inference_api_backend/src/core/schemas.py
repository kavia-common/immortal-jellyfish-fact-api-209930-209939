from datetime import datetime, timezone
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, HttpUrl


class SourceLink(BaseModel):
    """A link to a source with optional stance annotation."""
    url: HttpUrl = Field(..., description="HTTPS URL to the source article or paper")
    title: str = Field(..., description="Human-readable title of the source")
    stance: Optional[Literal["support", "refute"]] = Field(
        None, description="Whether this source supports or refutes the claim"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "url": "https://www.nature.com/articles/news.2010.490",
                "title": "Secrets of the 'immortal' jellyfish",
                "stance": "support",
            }
        }
    }


class FactResponse(BaseModel):
    """Response containing the immortal jellyfish fact, claim, and curated sources."""
    fact: str = Field(..., description="A concise fact about Turritopsis dohrnii")
    claim: str = Field(..., description="The central claim summarized for evaluation")
    supports: List[SourceLink] = Field(
        default_factory=list, description="List of sources that support the claim"
    )
    refutes: List[SourceLink] = Field(
        default_factory=list, description="List of sources that refute or nuance the claim"
    )
    retrieved_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the fact and sources were compiled (UTC)",
    )
    version: str = Field(..., description="API/version of the fact payload")

    model_config = {
        "json_schema_extra": {
            "example": {
                "fact": "Turritopsis dohrnii can revert its adult medusa stage back to a juvenile polyp stage under stress, a process termed transdifferentiation.",
                "claim": "The 'immortal jellyfish' can effectively avoid death by reverting to a younger life stage.",
                "supports": [
                    {
                        "url": "https://www.pnas.org/doi/10.1073/pnas.0701243104",
                        "title": "Transdifferentiation in Turritopsis spp.",
                        "stance": "support",
                    },
                    {
                        "url": "https://www.nature.com/articles/news.2010.490",
                        "title": "Secrets of the 'immortal' jellyfish",
                        "stance": "support",
                    },
                ],
                "refutes": [
                    {
                        "url": "https://www.smithsonianmag.com/science-nature/there-no-such-thing-immortal-jellyfish-180974035/",
                        "title": "There’s No Such Thing as an Immortal Jellyfish",
                        "stance": "refute",
                    }
                ],
                "retrieved_at": "2025-01-01T00:00:00Z",
                "version": "0.1.0",
            }
        }
    }
