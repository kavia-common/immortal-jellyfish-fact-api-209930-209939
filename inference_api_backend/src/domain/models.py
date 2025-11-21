from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class Source(BaseModel):
    """A source providing context for a fact."""
    title: str = Field(..., description="Human-readable title of the source")
    url: HttpUrl = Field(..., description="URL to the source")
    note: Optional[str] = Field(None, description="Short note on how the source supports or refutes the fact")


class FactResponse(BaseModel):
    """Response containing a fact and categorized sources."""
    fact: str = Field(..., description="The main fact text")
    supporting_sources: List[Source] = Field(..., description="Sources that support the fact")
    refuting_sources: List[Source] = Field(..., description="Sources that refute or contextualize the claim")


class HealthResponse(BaseModel):
    """Health/liveness response payload."""
    status: str = Field(..., description="Simple status indicator, e.g., 'ok'")


class ErrorResponse(BaseModel):
    """Generic error response."""
    detail: str = Field(..., description="Error details")
