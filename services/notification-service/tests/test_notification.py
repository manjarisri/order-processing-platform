from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_notify():
    response = client.post(
        "/notify",
        json={
            "order_id": "ORD-001",
            "message": "Your order has been processed"
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "order_id": "ORD-001",
        "status": "NOTIFICATION_SENT",
        "message": "Your order has been processed"
    }