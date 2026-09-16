import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AsyncPestVisionAgent:
    def __init__(self, max_concurrent_tasks=50):
        self.state = "IDLE"
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)

    async def _simulate_io(self):
        await asyncio.sleep(0.001)

    async def process_single(self, image_data: str):
        """Processes a single image asynchronously, gated by a semaphore."""
        async with self.semaphore:
            start = time.perf_counter()
            await self._simulate_io()

            latency_ms = (time.perf_counter() - start) * 1000

            return {
                "status": "success",
                "disease_name": "Wheat Rust",
                "confidence_score": 0.94,
                "latency_ms": latency_ms,
            }

    async def process_batch(self, image_batch: list):
        """Processes a batch of images concurrently with throughput control."""
        start = time.perf_counter()

        tasks = [self.process_single(img) for img in image_batch]
        results = await asyncio.gather(*tasks)

        total_latency_ms = (time.perf_counter() - start) * 1000
        logger.info(f"Batch of {len(image_batch)} processed in {total_latency_ms:.2f}ms")

        return results
