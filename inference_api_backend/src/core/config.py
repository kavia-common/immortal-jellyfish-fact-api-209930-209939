import os
from typing import Any, Dict, List


# PUBLIC_INTERFACE
def get_cors_settings() -> Dict[str, Any]:
    """Return CORS configuration settings.

    Defaults:
    - allow_origins: ["*"]
    - allow_credentials: True
    - allow_methods: ["GET"]
    - allow_headers: ["*"]

    Environment variables (optional):
    - CORS_ALLOW_ORIGINS: comma-separated list of origins
    - CORS_ALLOW_METHODS: comma-separated list of methods
    - CORS_ALLOW_HEADERS: comma-separated list of headers
    - CORS_ALLOW_CREDENTIALS: "true" or "false"
    """
    origins_env = os.getenv("CORS_ALLOW_ORIGINS")
    methods_env = os.getenv("CORS_ALLOW_METHODS")
    headers_env = os.getenv("CORS_ALLOW_HEADERS")
    creds_env = os.getenv("CORS_ALLOW_CREDENTIALS")

    def parse_list(val: str | None, default: List[str]) -> List[str]:
        if not val:
            return default
        return [v.strip() for v in val.split(",") if v.strip()]

    allow_origins = parse_list(origins_env, ["*"])
    allow_methods = parse_list(methods_env, ["GET"])
    allow_headers = parse_list(headers_env, ["*"])
    allow_credentials = True if (creds_env or "true").lower() == "true" else False

    return {
        "allow_origins": allow_origins,
        "allow_methods": allow_methods,
        "allow_headers": allow_headers,
        "allow_credentials": allow_credentials,
    }
