import os


# PUBLIC_INTERFACE
def get_version() -> str:
    """Return the application version.

    Reads from environment variable APP_VERSION if present, else falls back to semantic default.
    """
    return os.getenv("APP_VERSION", "1.0.0")
