import asyncio
import time
from api.async_agent import AsyncPestVisionAgent

async def test_throughput():
    # Initialize agent with a tuned concurrency limit
    agent = AsyncPestVisionAgent(max_concurrent_tasks=100)
    total_requests = 500
    batch = [f"mock_image_{i}" for i in range(total_requests)]
    
    print(f"🚀 Starting Throughput Profiling for {total_requests} concurrent requests...\n")
    start_time = time.perf_counter()
    
    # Fire 500 requests at once
    results = await agent.process_batch(batch)
    
    total_time = time.perf_counter() - start_time
    rps = total_requests / total_time
    
    print(f"📊 --- THROUGHPUT RESULTS ---")
    print(f"Total Time: {total_time:.2f}s")
    print(f"Throughput: {rps:.2f} Requests Per Second (RPS)")
    
    if rps > 150:
        print("✅ SLA Passed: High throughput achieved without CPU thrashing.")
    else:
        print("⚠️ SLA Warning: Throughput needs further optimization.")

if __name__ == "__main__":
    asyncio.run(test_throughput())
