import time
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.agent import PestVisionAgent

logging.getLogger().setLevel(logging.ERROR) # Hide standard logs to focus on benchmark output

def run_benchmark(num_requests=5):
    print(f"🚀 Starting Agent Benchmark profiling {num_requests} sequential requests...\n")
    agent = PestVisionAgent()
    
    start_time = time.time()
    successful_requests = 0
    fallback_triggers = 0
    
    for i in range(num_requests):
        req_start = time.time()
        result = agent.process_diagnosis_workflow(f"mock_image_data_{i}")
        req_latency = time.time() - req_start
        
        status = result.get("status")
        final_advice = result.get("data", {}).get("final_advice", "")
        tokens = result.get("data", {}).get("session_tokens_used", 0)
        
        if "FALLBACK" in final_advice:
            fallback_triggers += 1
            print(f"⚠️ Req {i+1}: FALLBACK TRIGGERED | Latency: {req_latency:.2f}s")
        elif status == "success":
            successful_requests += 1
            print(f"✅ Req {i+1}: SUCCESS | Tokens: {tokens} | Latency: {req_latency:.2f}s")
        else:
            print(f"❌ Req {i+1}: ERROR | Latency: {req_latency:.2f}s")
            
    total_latency = time.time() - start_time
    
    print("\n📊 --- BENCHMARK RESULTS ---")
    print(f"Total Latency:       {total_latency:.2f}s")
    print(f"Avg Latency/Req:     {(total_latency/num_requests):.2f}s")
    print(f"Total Tokens Used:   {agent.total_tokens_used}")
    print(f"Successful API Hits: {successful_requests}/{num_requests}")
    print(f"Fallbacks Triggered: {fallback_triggers}/{num_requests}")

if __name__ == "__main__":
    run_benchmark()
