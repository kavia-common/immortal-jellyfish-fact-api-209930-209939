import os
from typing import List


class Settings:
    """Application settings sourced from environment variables with safe defaults."""
    # App metadata
    APP_NAME: str = os.getenv("APP_NAME", "Immortal Jellyfish Inference API")
    APP_DESCRIPTION: str = os.getenv(
        "APP_DESCRIPTION",
        "An API that returns a curated fact about the 'immortal jellyfish' (Turritopsis dohrnii) "
        "with links to supporting and refuting sources."
    )
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")

    # CORS
    CORS_ALLOW_ORIGINS: List[str] = (
        os.getenv("CORS_ALLOW_ORIGINS", "*").split(",") if os.getenv("CORS_ALLOW_ORIGINS") else ["*"]
    )
    CORS_ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    CORS_ALLOW_METHODS: List[str] = (
        os.getenv("CORS_ALLOW_METHODS", "*").split(",") if os.getenv("CORS_ALLOW_METHODS") else ["*"]
    )
    CORS_ALLOW_HEADERS: List[str] = (
        os.getenv("CORS_ALLOW_HEADERS", "*").split(",") if os.getenv("CORS_ALLOW_HEADERS") else ["*"]
    )


settings = Settings()
