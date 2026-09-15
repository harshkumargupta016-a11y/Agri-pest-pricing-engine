import pytest
import time
from api.async_agent import AsyncPestVisionAgent

@pytest.mark.asyncio
async def test_sla_latency_single_request():
    agent = AsyncPestVisionAgent()
    start = time.perf_counter()
    
    result = await agent.process_single("mock_image_1")
    latency_ms = (time.perf_counter() - start) * 1000
    
    # SLA Gate: Must be under 150ms
    assert latency_ms < 150, f"SLA Violation: Latency was {latency_ms:.2f}ms"
    assert result["status"] == "success"

@pytest.mark.asyncio
async def test_sla_latency_batch_concurrency():
    agent = AsyncPestVisionAgent()
    start = time.perf_counter()
    
    # Process 5 requests concurrently
    batch = ["img1", "img2", "img3", "img4", "img5"]
    results = await agent.process_batch(batch)
    
    latency_ms = (time.perf_counter() - start) * 1000
    
    # SLA Gate: Entire batch must finish under 150ms due to concurrency
    assert latency_ms < 150, f"Batch SLA Violation: Latency was {latency_ms:.2f}ms"
    assert len(results) == 5
