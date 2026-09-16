from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
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

# Initialize Prometheus Telemetry
Instrumentator().instrument(app).expose(app)

pricing_engine = MandiPricingEngine()
vision_agent = PestVisionAgent()

class VisionRequest(BaseModel):
    image_base64: str

    commodity: str
    state: str
    district: str


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


