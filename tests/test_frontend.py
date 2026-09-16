import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_frontend_loads_and_is_responsive():
    """Verify the static UI serves correctly and contains mobile-responsive meta tags."""
    response = client.get("/ui/")
    
    # Assert the endpoint serves HTML successfully
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    
    html_content = response.text
    
    # Assert UI title and structure loads
    assert "Agri-Pest & Mandi Dashboard" in html_content
    
    # Assert strict mobile-responsiveness viewport tags exist
    assert 'name="viewport"' in html_content
    assert 'width=device-width' in html_content
    
    # Assert streaming and telemetry endpoints are wired up
    assert '/api/v1/metrics/live' in html_content
    assert '/api/v1/diagnose/stream' in html_content
    
    print("\n✅ Frontend Integration Test Passed: Responsive UI is fully operational.")
