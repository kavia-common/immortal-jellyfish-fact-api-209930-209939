from fastapi.testclient import TestClient
from src.api.main import app


def test_health_ok_status_code_and_payload():
    """Verify that /health returns 200 and the expected JSON payload."""
    client = TestClient(app)
    resp = client.get("/health")

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert data == {"status": "ok"}
