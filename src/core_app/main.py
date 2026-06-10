from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
from typing import Optional
import os
import httpx

app = FastAPI(
    title="Smart Campus — Core Business Policy API",
    version=os.getenv("SERVICE_VERSION", "v0.1.0-team-core"),
    description="Lab 05 — Core Business Policy Engine with Docker Compose"
)

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=422, content={"status": 422, "title": "Validation Error", "detail": str(exc.errors()[0]["msg"])})

AUTH_TOKEN = os.getenv("AUTH_TOKEN", "lab-compose-token")
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:9000")

security = HTTPBearer(auto_error=False)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials or credentials.credentials != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials.credentials

# In-memory policy store
POLICIES = {
    "POL-2026-001": {
        "policyId": "POL-2026-001",
        "gateId": "GATE-01",
        "allowedRoles": ["STUDENT", "STAFF"],
        "timeRestriction": {
            "restrictionType": "TIME_WINDOW",
            "startTime": "07:00",
            "endTime": "22:00",
            "daysOfWeek": ["MON", "TUE", "WED", "THU", "FRI"]
        },
        "active": True,
        "updatedAt": "2026-05-01T00:00:00Z"
    }
}

ACCESS_LOGS = []

class AccessCheckRequest(BaseModel):
    cardId: str

    @field_validator("cardId")
    @classmethod
    def validate_card_id(cls, v):
        import re
        if not re.match(r"^RFID-[A-Z0-9\-]{1,28}$", v):
            raise ValueError("cardId must match pattern ^RFID-[A-Z0-9\-]{1,28}$")
        return v
    gateId: str
    direction: str
    timestamp: str

class AccessLogRequest(BaseModel):
    cardId: str
    gateId: str
    direction: str
    decision: str
    reason: Optional[str] = None
    timestamp: str

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "core-business",
        "version": os.getenv("SERVICE_VERSION", "v0.1.0-team-core"),
        "time": datetime.now(timezone.utc).isoformat()
    }

@app.post("/policy/access-check", dependencies=[Depends(verify_token)])
def access_check(req: AccessCheckRequest):
    import re as _re
    if not _re.match(r"^RFID-[A-Z0-9\-]{1,28}$", req.cardId):
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=422, content={"status": 422, "title": "Validation Error", "detail": "cardId format invalid"})
    policy = next((p for p in POLICIES.values() if p["gateId"] == req.gateId), None)
    if not policy or not policy["active"]:
        return {
            "cardId": req.cardId,
            "gateId": req.gateId,
            "decision": "DENY",
            "reason": "No active policy for this gate",
            "policyId": None,
            "checkedAt": datetime.now(timezone.utc).isoformat()
        }
    return {
        "cardId": req.cardId,
        "gateId": req.gateId,
        "decision": "ALLOW",
        "reason": None,
        "policyId": policy["policyId"],
        "checkedAt": datetime.now(timezone.utc).isoformat()
    }

@app.get("/policy/rules", dependencies=[Depends(verify_token)])
def get_policy_rules():
    return {
        "items": list(POLICIES.values()),
        "nextCursor": None,
        "hasMore": False
    }

@app.get("/policy/rules/{policyId}", dependencies=[Depends(verify_token)])
def get_policy_rule(policyId: str):
    policy = POLICIES.get(policyId)
    if not policy:
        raise HTTPException(status_code=404, detail=f"Policy {policyId} not found")
    return policy

@app.post("/access-log", status_code=201, dependencies=[Depends(verify_token)])
def create_access_log(req: AccessLogRequest):
    import uuid
    log_id = str(uuid.uuid4())
    ACCESS_LOGS.append({"logId": log_id, **req.model_dump()})
    return {
        "logId": log_id,
        "acceptedAt": datetime.now(timezone.utc).isoformat()
    }

@app.post("/ai/predict", dependencies=[Depends(verify_token)])
async def proxy_ai_predict(req: AccessCheckRequest):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{AI_SERVICE_URL}/predict", json={"cardId": req.cardId}, timeout=5)
            return resp.json()
        except Exception:
            return {"cardId": req.cardId, "label": "UNKNOWN", "error": "AI service unavailable"}
