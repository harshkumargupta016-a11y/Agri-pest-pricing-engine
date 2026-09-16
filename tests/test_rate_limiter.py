import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.rate_limiter import redis_client

# Use the synchronous TestClient for integration testing HTTP routes
client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_redis_state():
    """Ensure a clean Redis database before each test runs to avoid cross-test contamination."""
    try:
        redis_client.flushdb()
    except Exception:
        pass
    yield

def test_distributed_rate_limiter_enforces_sla():
    payload = {"image_base64": "mock_image_data"}
    
    # Simulate a user maxing out their allowed 50 Requests Per Minute (RPM)
    for i in range(50):
        response = client.post("/api/v1/diagnose", json=payload)
        assert response.status_code == 200, f"Request {i+1} failed prematurely!"
        
    # The 51st request MUST trigger the Redis SLA protection
    response = client.post("/api/v1/diagnose", json=payload)
    
    # Assert that the load shedding mechanism successfully activated
    assert response.status_code == 429
    assert "SLA Protection Active" in response.json()["detail"]
    print("\n✅ SLA Integration Test Passed: Rate Limiter successfully intercepted excess traffic!")

def test_mandi_pricing_rate_limit():
    payload = {"commodity": "Wheat", "state": "MP", "district": "Indore"}
    
    # Quickly hit the pricing endpoint 50 times
    for _ in range(50):
        client.post("/api/v1/mandi/prices", json=payload)
        
    # The 51st request should be blocked
    response = client.post("/api/v1/mandi/prices", json=payload)
    assert response.status_code == 429
