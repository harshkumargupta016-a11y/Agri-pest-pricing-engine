import pytest
from api.agent import PestVisionAgent

def test_agent_initial_state():
    agent = PestVisionAgent()
    assert agent.state == "IDLE"

def test_vector_search_transition():
    agent = PestVisionAgent()
    result = agent.vector_search("wheat rust")
    assert "Tebuconazole" in result
    assert agent.state == "SEARCHING_VECTORS"

def test_agent_fallback_mechanism(monkeypatch):
    agent = PestVisionAgent()
    
    # Mock the external API to force a timeout/ConnectionError
    def mock_api_call(context):
        raise ConnectionError("502 Bad Gateway: External API Provider Timeout")
    
    # Inject the mock failure into the agent
    monkeypatch.setattr(agent, "_simulate_external_llm_call", mock_api_call)
    
    # Run the workflow
    result = agent.process_diagnosis_workflow("mock_image_data")
    
    # Verify the fallback caught the error and completed successfully
    assert result["status"] == "success"
    assert result["workflow_state"] == "COMPLETED"
    assert "FALLBACK TRIGGERED" in result["data"]["final_advice"]
