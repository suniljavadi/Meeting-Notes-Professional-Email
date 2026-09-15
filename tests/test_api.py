from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_api():
    response = client.post("/api/v1/analyze", json={"transcript": "Sunil will prepare the checklist by Friday."})
    assert response.status_code == 200
    payload = response.json()
    assert payload["analysis"]["action_items"][0]["owner"] == "Sunil"
    assert "request_id" in payload


def test_rejects_empty_transcript():
    response = client.post("/api/v1/analyze", json={"transcript": "   "})
    assert response.status_code == 422


def test_generate_email_api():
    response = client.post("/api/v1/generate-email", json={"transcript": "Maya will send the plan by Wednesday.", "tone": "friendly"})
    assert response.status_code == 200
    assert response.json()["subject"] == "Meeting follow-up"
