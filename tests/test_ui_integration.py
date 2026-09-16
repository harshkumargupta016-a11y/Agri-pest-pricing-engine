from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_mandi_pricing_api_integration():
    """Verifies the UI can successfully fetch Mandi pricing data."""
    payload = {"commodity": "Soybean", "state": "MP", "district": "Indore"}
    response = client.post("/api/v1/mandi/prices", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["commodity"] == "Soybean"
    assert "price_inr_per_quintal" in data["data"]

def test_streaming_endpoint_health():
    """Verifies the SSE streaming endpoint returns the correct headers and status."""
    payload = {"image_base64": "mock_image"}
    
    # We use stream=True to test Server-Sent Events
    with client.stream("POST", "/api/v1/diagnose/stream", json=payload) as response:
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
