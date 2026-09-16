from locust import HttpUser, task, between
import logging

class PestVisionLoadTest(HttpUser):
    # Simulate users waiting between 0.1 and 0.5 seconds between requests
    wait_time = between(0.1, 0.5)

    @task
    def test_diagnose_endpoint_sla(self):
        payload = {"image_base64": "mock_base64_image_data_for_continuous_load"}
        
        # Fire request and catch the response to evaluate the SLA
        with self.client.post("/api/v1/diagnose", json=payload, catch_response=True) as response:
            latency = response.elapsed.total_seconds()
            
            if response.status_code != 200:
                response.failure(f"Failed with status {response.status_code}")
            elif latency > 0.15:
                # SLA Gate: Fail the request if it breaches 150ms
                response.failure(f"SLA Violation: Latency was {latency:.3f}s (>150ms)")
            else:
                response.success()
                
    @task(3) # This task runs 3x more frequently
    def test_mandi_pricing_endpoint(self):
        payload = {"commodity": "Wheat", "state": "MP", "district": "Indore"}
        self.client.post("/api/v1/mandi/prices", json=payload)
