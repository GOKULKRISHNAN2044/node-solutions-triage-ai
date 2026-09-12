from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import TriageRequest
from service.triage_service import TriageService
from repositories.database import get_db
from utils.response_helper import ok, bad_request, server_error

router = APIRouter(prefix="/api", tags=["Triage"])
service = TriageService()


@router.post("/triage", summary="Analyze and triage an incoming request")
def triage_request(payload: TriageRequest, db: Session = Depends(get_db)):
    """
    Accepts a raw business request, runs it through the AI triage pipeline,
    saves the result, and returns the structured triage output.
    """
    if not payload.request_text or len(payload.request_text.strip()) < 10:
        return bad_request("Request text must be at least 10 characters.")

    try:
        result = service.process_request(db, payload.request_text.strip())
        return ok(result.model_dump(), "Request triaged successfully.")
    except ValueError as e:
        return bad_request(str(e))
    except RuntimeError as e:
        return server_error(str(e))


@router.get("/history", summary="Get all past triage records")
def get_history(db: Session = Depends(get_db)):
    """
    Returns all previously processed triage records ordered by newest first.
    """
    try:
        records = service.get_history(db)
        return ok([r.model_dump() for r in records], f"{len(records)} records found.")
    except Exception as e:
        return server_error(str(e))
