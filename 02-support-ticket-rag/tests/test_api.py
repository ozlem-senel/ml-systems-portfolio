import os

from fastapi.testclient import TestClient

os.environ["LLM_PROVIDER"] = "mock"

from src.api import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["pipeline_ready"] is True


def test_process_payment_ticket():
    with TestClient(app) as client:
        response = client.post(
            "/process",
            json={
                "ticket_id": "TEST-001",
                "subject": "Payment failed",
                "description": "My credit card was declined but I have sufficient funds",
            },
        )

    assert response.status_code == 200
    result = response.json()
    assert result["ticket_id"] == "TEST-001"
    assert result["predicted_category"] == "payment"
    assert result["retrieved_documents"]


def test_validation_error_for_incomplete_ticket():
    with TestClient(app) as client:
        response = client.post("/process", json={"ticket_id": "TEST-002"})
    assert response.status_code == 422
