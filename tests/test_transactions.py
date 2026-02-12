from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_create_transaction():
    response = client.post(
        "/transaction",
        json={"user_id": 1, "amount": 5000}
    )
    assert response.status_code == 200
    assert "risk" in response.json()
