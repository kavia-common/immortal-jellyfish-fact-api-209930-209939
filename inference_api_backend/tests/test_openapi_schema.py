from fastapi.testclient import TestClient
from src.api.main import app


def test_openapi_includes_fact_schema_and_path():
    """Validate /openapi.json exists and includes FactResponse schema and /v1/fact path."""
    client = TestClient(app)
    resp = client.get("/openapi.json")
    assert resp.status_code == 200

    schema = resp.json()
    # Basic OpenAPI structure
    assert "openapi" in schema
    assert "paths" in schema
    assert "components" in schema

    # Path existence
    assert "/v1/fact" in schema["paths"], "Missing /v1/fact path in OpenAPI schema"

    # FactResponse schema existence (under components.schemas)
    components = schema.get("components") or {}
    schemas = components.get("schemas") or {}
    assert "FactResponse" in schemas, "Missing FactResponse schema in OpenAPI components"

    # Optional: sanity-check some properties on FactResponse
    fact_resp = schemas["FactResponse"]
    props = fact_resp.get("properties", {})
    for prop in ("fact", "claim", "supports", "refutes", "retrieved_at", "version"):
        assert prop in props, f"Missing property on FactResponse: {prop}"
