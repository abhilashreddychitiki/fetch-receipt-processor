import sys
import os

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # Now this should work

from fastapi.testclient import TestClient

client = TestClient(app)

def test_process_receipt():
    payload = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"}
        ],
        "total": "9.00"
    }
    response = client.post("/receipts/process", json=payload)
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_points():
    payload = {
        "retailer": "Target",
        "purchaseDate": "2022-02-02",
        "purchaseTime": "14:00",
        "items": [{"shortDescription": "Apple", "price": "1.50"}],
        "total": "1.50"
    }
    response = client.post("/receipts/process", json=payload)
    assert response.status_code == 200
    receipt_id = response.json()["id"]

    response = client.get(f"/receipts/{receipt_id}/points")
    assert response.status_code == 200
    assert "points" in response.json()