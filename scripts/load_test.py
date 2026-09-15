import asyncio
import logging
import tracemalloc
from api.async_agent import AsyncPestVisionAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def continuous_load_test(iterations=100, batch_size=10):
    print(f"🚀 Starting Continuous Load Test: {iterations} iterations of {batch_size} concurrent requests...\n")
    agent = AsyncPestVisionAgent()
    
    # Start tracing memory allocation
    tracemalloc.start()
    
    for i in range(iterations):
        batch = [f"mock_image_{i}_{j}" for j in range(batch_size)]
        await agent.process_batch(batch)
        
        # Log memory usage every 20 iterations
        if i % 20 == 0:
            current, peak = tracemalloc.get_traced_memory()
            logger.info(f"Iteration {i} | Memory: {current / 10**6:.3f}MB | Peak: {peak / 10**6:.3f}MB")
            
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print("\n📊 --- CONTINUOUS LOAD TEST COMPLETE ---")
    print(f"Final Memory Usage: {current / 10**6:.3f}MB")
    print(f"Peak Memory Usage:  {peak / 10**6:.3f}MB")
    
    # Basic heuristic to warn about memory leaks
    if (current / peak) > 0.8 and current > 1000000:
        print("⚠️ WARNING: Potential memory leak detected. Memory is not being released.")
    else:
        print("✅ Memory stable. No significant leaks detected under continuous load.")

if __name__ == "__main__":
    asyncio.run(continuous_load_test())
