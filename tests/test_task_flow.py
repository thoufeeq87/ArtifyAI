import os
import time
import pytest
from fastapi.testclient import TestClient
from services.api.app.main import app

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

@pytest.mark.integration
def test_enqueue_and_status():
    client = TestClient(app)

    r = client.post("/api/v1/tasks/enqueue", json={"type": "add", "params": {"x": 2, "y": 40}})
    assert r.status_code == 200
    task_id = r.json()["task_id"]
    assert task_id

    for _ in range(30):
        s = client.get(f"/api/v1/tasks/{task_id}")
        data = s.json()
        if data["status"] == "SUCCESS":
            assert data["result"] == 42
            return
        time.sleep(0.5)

    pytest.fail("Task did not complete in time")
