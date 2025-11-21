import re
from fastapi.testclient import TestClient

from src.api.main import app

# Instantiate a single client for test session
client = TestClient(app)


def test_root_liveness_ok():
    # GET /
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    # Expect simple schema with status: "ok"
    assert isinstance(data, dict)
    assert data.get("status") == "ok"


def test_health_ok():
    # GET /health
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    # Expect simple schema with status: "ok"
    assert isinstance(data, dict)
    assert data.get("status") == "ok"


def _is_valid_http_url(url: str) -> bool:
    # Simple URL validation using regex; server already validates via Pydantic.
    pattern = re.compile(
        r"^https?://[^\s/$.?#].[^\s]*$",
        re.IGNORECASE,
    )
    return bool(pattern.match(url))


def test_get_immortal_jellyfish_fact_structure_and_values():
    # GET /v1/facts/immortal-jellyfish
    resp = client.get("/v1/facts/immortal-jellyfish")
    assert resp.status_code == 200

    payload = resp.json()

    # Top-level structure
    assert isinstance(payload, dict)
    assert "fact" in payload
    assert "supporting_sources" in payload
    assert "refuting_sources" in payload

    # Fact should be a non-empty string
    assert isinstance(payload["fact"], str)
    assert payload["fact"].strip() != ""

    # supporting_sources/refuting_sources should be arrays
    supporting = payload["supporting_sources"]
    refuting = payload["refuting_sources"]
    assert isinstance(supporting, list)
    assert isinstance(refuting, list)

    # Expect at least one entry in each list based on service implementation
    assert len(supporting) > 0
    assert len(refuting) > 0

    # Validate all source entries
    for group in (supporting, refuting):
        for source in group:
            # Required keys
            assert "title" in source
            assert "url" in source
            # Optional note can be null in the schema, but implementation returns non-empty notes
            assert "note" in source

            title = source["title"]
            url = source["url"]
            note = source["note"]

            assert isinstance(title, str) and title.strip() != ""
            assert isinstance(url, str) and _is_valid_http_url(url)

            # Our curated dataset returns non-empty notes
            assert isinstance(note, str)
            assert note.strip() != ""
