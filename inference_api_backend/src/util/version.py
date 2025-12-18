# PUBLIC_INTERFACE
def get_version(default: str = "0.1.0") -> str:
    """Return application version from environment or default.

    Attempts to read version from environment variable APP_VERSION first.
    Falls back to provided default if not available.

    Returns:
        str: Version string.
    """
    # Keep implementation self-contained without external packages.
    # Using environment variable to optionally override version.
    import os

    return os.getenv("APP_VERSION", default)
