from fastapi import FastAPI

app = FastAPI(title="Agri-Pest Pricing Engine")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}


__all__ = ["app"]
