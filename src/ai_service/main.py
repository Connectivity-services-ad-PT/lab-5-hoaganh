from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone
import os

app = FastAPI(title="AI Mock Service", version="1.0.0")

class PredictRequest(BaseModel):
    cardId: str
    imageData: str | None = None

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-mock",
        "version": os.getenv("SERVICE_VERSION", "v0.1.0-team-core"),
        "time": datetime.now(timezone.utc).isoformat()
    }

@app.post("/predict")
def predict(req: PredictRequest):
    return {
        "cardId": req.cardId,
        "identityConfidence": 0.97,
        "label": "AUTHORIZED",
        "modelVersion": "mock-v1",
        "processedAt": datetime.now(timezone.utc).isoformat()
    }
