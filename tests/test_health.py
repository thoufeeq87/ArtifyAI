from fastapi.testclient import TestClient

from services.api.app.main import app


def test_health() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
