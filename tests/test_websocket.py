import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_websocket_telemetry_connection():
    """Verifies the live telemetry WebSocket connects and streams the correct agent metrics."""
    with client.websocket_connect("/api/v1/metrics/live") as websocket:
        # Wait for and receive the first JSON payload broadcasted by the server
        data = websocket.receive_json()
        
        # Assert the payload matches our strict schema requirements
        assert "state" in data
        assert "tokens" in data
        assert "circuit_breaker" in data
        
        # Assert initial state types
        assert isinstance(data["state"], str)
        assert isinstance(data["tokens"], int)
        assert isinstance(data["circuit_breaker"], bool)
        
        print("\n✅ WebSocket Integration Test Passed: Live telemetry streaming is functional!")
