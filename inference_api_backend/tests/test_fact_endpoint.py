from urllib.parse import urlparse

from fastapi.testclient import TestClient
from src.api.main import app


def _is_https_url(u: str) -> bool:
    """Helper to validate HTTPS URLs."""
    try:
        parsed = urlparse(u)
    except Exception:
        return False
    return parsed.scheme == "https" and bool(parsed.netloc)


def test_fact_response_schema_and_content():
    """
    Validate the /v1/fact endpoint:
    - returns 200
    - contains required keys
    - supports/refutes are lists with at least one item each
    - each SourceLink has url (https), title (non-empty), and stance in {'support','refute'} or None
    """
    client = TestClient(app)
    resp = client.get("/v1/fact")
    assert resp.status_code == 200

    data = resp.json()
    # Required top-level keys
    for key in ("fact", "claim", "supports", "refutes", "retrieved_at", "version"):
        assert key in data, f"Missing key: {key}"

    assert isinstance(data["fact"], str) and data["fact"]
    assert isinstance(data["claim"], str) and data["claim"]
    assert isinstance(data["supports"], list)
    assert isinstance(data["refutes"], list)
    # At least one support and one refute
    assert len(data["supports"]) >= 1
    assert len(data["refutes"]) >= 1

    # Validate SourceLink items
    for item in data["supports"] + data["refutes"]:
        assert isinstance(item, dict)
        assert "url" in item and "title" in item
        assert isinstance(item["title"], str) and item["title"].strip() != ""
        assert _is_https_url(item["url"])

        stance = item.get("stance")
        # stance can be "support", "refute", or None (per schema)
        assert stance in ("support", "refute", None)
