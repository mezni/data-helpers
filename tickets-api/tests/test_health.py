from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/api/v1/")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["version"] == "1.0.0"
