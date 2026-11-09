from fastapi.testclient import TestClient
from app.main import app


def test_health_and_advisor_records():
    with TestClient(app) as client:
        health = client.get("/health/ready")
        assert health.status_code == 200
        response = client.get("/api/v1/advisors/GP00334146/bob")
        assert response.status_code == 200
        body = response.json()
        assert body["advisor_id"] == "GP00334146"
        assert body["summary"]["client_count"] > 0
        assert all(r["advisor_id"] == "GP00334146" for r in body["records"])


def test_unknown_advisor_returns_404():
    with TestClient(app) as client:
        response = client.get("/api/v1/advisors/NOT-A-REAL-ADVISOR/bob")
        assert response.status_code == 404
