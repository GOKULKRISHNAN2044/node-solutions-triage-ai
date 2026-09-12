from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any
from datetime import datetime
import uuid


# ── Request ──────────────────────────────────────────────────────────────────

class TriageRequest(BaseModel):
    request_text: str


# ── Response (from Gemini) ────────────────────────────────────────────────────

class TriageResult(BaseModel):
    id: Optional[int] = None
    raw_input: str
    summary: str
    category: str
    priority: str
    priority_reason: str
    route: str
    draft_response: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ── Standard API Envelope ─────────────────────────────────────────────────────

class Error(BaseModel):
    code: str
    message: str
    error_code_id: Optional[str] = None


class APIResponse(BaseModel):
    data: Any = None
    errors: List[Error] = []
    status_code: int = 200
    request_id: str = ""
    message: str = ""

    model_config = ConfigDict(from_attributes=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def success_response(data: Any, message: str = "Success") -> dict:
    return APIResponse(
        data=data,
        errors=[],
        status_code=200,
        request_id=str(uuid.uuid4()),
        message=message,
    ).model_dump()


def error_response(code: str, message: str, status_code: int = 500) -> dict:
    return APIResponse(
        data=None,
        errors=[Error(code=code, message=message)],
        status_code=status_code,
        request_id=str(uuid.uuid4()),
        message=message,
    ).model_dump()
