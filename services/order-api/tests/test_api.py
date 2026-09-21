from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_check():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_order():

    response = client.post(
        "/orders",
        json={
            "product": "Laptop",
            "quantity": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product"] == "Laptop"
    assert data["quantity"] == 1
    assert data["status"] == "CREATED"


def test_invalid_quantity():

    response = client.post(
        "/orders",
        json={
            "product": "Laptop",
            "quantity": 0
        }
    )

    assert response.status_code == 400