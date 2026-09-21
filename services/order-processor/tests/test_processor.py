from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_process_order():
    response = client.post(
        "/process",
        json={"order_id": "ORD-001"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "order_id": "ORD-001",
        "status": "PROCESSED"
    }