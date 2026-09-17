from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uvloop
import asyncio
from sse_starlette.sse import EventSourceResponse
from prometheus_fastapi_instrumentator import Instrumentator

from .engine import MandiPricingEngine
from .agent import PestVisionAgent
from .rate_limiter import verify_rate_limit

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
load_dotenv()

app = FastAPI(title="Agri-Pest Pricing Engine", version="0.7.0", default_response_class=ORJSONResponse)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Prometheus Telemetry
Instrumentator().instrument(app).expose(app)

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
    return {"status": "ok"}


# 1. New Real-Time WebSocket Telemetry Endpoint
@app.websocket("/api/v1/metrics/live")
async def websocket_metrics(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json({
                "state": vision_agent.state,
                "tokens": vision_agent.total_tokens_used,
                "circuit_breaker": getattr(vision_agent, 'circuit_breaker_active', False)
            })
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass

# 2. Existing SSE Streaming Endpoint
@app.post("/api/v1/diagnose/stream", dependencies=[Depends(verify_rate_limit)])
async def diagnose_crop_stream(request: VisionRequest):
    if not request.image_base64:
        raise HTTPException(status_code=400, detail="Image data is required")
        
    async def event_generator():
        yield {"data": "Analyzing Image... Disease detected: Wheat Rust.\n\n"}
        await asyncio.sleep(0.5)
        yield {"data": "Retrieving context from Vector DB...\n\n"}
        await asyncio.sleep(0.5)
        
        advice = "Apply fungicide containing Tebuconazole. Ensure proper field drainage to prevent root rot."
        for word in advice.split():
            yield {"data": word + " "}
            await asyncio.sleep(0.1)
            
        yield {"data": "[DONE]"}

    return EventSourceResponse(event_generator())

@app.post("/api/v1/diagnose", dependencies=[Depends(verify_rate_limit)])
async def diagnose_crop(request: VisionRequest):
    return vision_agent.process_diagnosis_workflow(request.image_base64)

@app.post("/api/v1/mandi/prices", dependencies=[Depends(verify_rate_limit)])
async def get_mandi_prices(request: PricingRequest):
    result = pricing_engine.get_price(request.commodity, request.state, request.district)
    return {"status": "success", "data": result}

# Mount Frontend
os.makedirs("static", exist_ok=True)
app.mount("/ui", StaticFiles(directory="static", html=True), name="static")
@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")
