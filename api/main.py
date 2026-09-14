from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from .engine import MandiPricingEngine
from .agent import PestVisionAgent

load_dotenv()

app = FastAPI(title="Agri-Pest Pricing Engine", version="0.3.0")
pricing_engine = MandiPricingEngine()
vision_agent = PestVisionAgent()

class VisionRequest(BaseModel):
    image_base64: str

class PricingRequest(BaseModel):
    commodity: str
    state: str
    district: str

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": {"api": "online", "redis": "configured", "agent": "ready"}}

@app.get("/api/v1/agent/metrics")
async def get_agent_metrics():
    """Expose core algorithm profiling and state machine status."""
    return {
        "status": "success",
        "data": {
            "current_state": vision_agent.state,
            "total_tokens_used": vision_agent.total_tokens_used,
            "circuit_breaker_active": getattr(vision_agent, 'circuit_breaker_active', False),
            "knowledge_base_size": len(vision_agent.knowledge_base)
        }
    }

@app.post("/api/v1/diagnose")
async def diagnose_crop(request: VisionRequest):
    if not request.image_base64:
        raise HTTPException(status_code=400, detail="Image data is required")
    result = vision_agent.process_diagnosis_workflow(request.image_base64)
    return result

@app.post("/api/v1/mandi/prices")
async def get_mandi_prices(request: PricingRequest):
    result = pricing_engine.get_price(request.commodity, request.state, request.district)
    return {"status": "success", "data": result}
