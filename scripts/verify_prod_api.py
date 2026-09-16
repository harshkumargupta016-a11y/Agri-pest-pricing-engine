import requests
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# This would be swapped dynamically in CI/CD with your actual Cloud Run/AWS domain
PROD_URL = "https://agri-pest-engine-production.up.railway.app/health"

def verify_production_deployment():
    logger.info(f"🔍 Verifying Public HTTPS API Availability at: {PROD_URL}")
    
    try:
        # We enforce a strict timeout to ensure the SLA holds even on initial cold starts
        response = requests.get(PROD_URL, timeout=10)
        
        if response.status_code == 200:
            logger.info("✅ SUCCESS: Production API is live, secured via HTTPS, and responding perfectly!")
            logger.info(f"Payload: {response.json()}")
        else:
            logger.warning(f"⚠️ WARNING: API returned status {response.status_code}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ ERROR: Could not connect to production API. The container might still be deploying. Details: {e}")
        # In a real pipeline, we might fail the step here if the deployment didn't expose the port
        sys.exit(1)

if __name__ == "__main__":
    verify_production_deployment()
