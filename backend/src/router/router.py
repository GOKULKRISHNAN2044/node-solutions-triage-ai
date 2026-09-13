from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import TriageRequest
from service.triage_service import TriageService
from repositories.database import get_db
from repositories.user_repo import UserRepository
from models.models import TriageRequest, LoginRequest
from utils.response_helper import ok, bad_request, server_error, unauthorized

router = APIRouter(prefix="/api", tags=["Triage"])
service = TriageService()
user_repo = UserRepository()


# ── Auth Endpoints ────────────────────────────────────────────────────────────

@router.post("/auth/login", tags=["Auth"], summary="Authenticate user with username and password")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    if not payload.username or not payload.password:
        return bad_request("Username and password are required.")

    user = user_repo.verify_credentials(db, payload.username, payload.password)
    if not user:
        return unauthorized("Invalid username or password.")

    return ok({
        "user": {
            "id": user.id,
            "username": user.username,
        },
        "token": f"bearer_{user.username}_{user.id}",
    }, "Authentication successful.")


@router.post("/auth/register", tags=["Auth"], summary="Register a new user")
def register(payload: LoginRequest, db: Session = Depends(get_db)):
    if not payload.username or not payload.password:
        return bad_request("Username and password are required.")
    if len(payload.password) < 6:
        return bad_request("Password must be at least 6 characters.")

    existing = user_repo.get_by_username(db, payload.username)
    if existing:
        return bad_request("Username already exists.")

    user = user_repo.create_user(db, payload.username, payload.password)
    return ok({
        "user": {
            "id": user.id,
            "username": user.username,
        }
    }, "User registered successfully.")


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
        return ok(result.model_dump(mode="json"), "Request triaged successfully.")
    except ValueError as e:
        return bad_request(str(e))
    except Exception as e:
        return server_error(str(e))


@router.get("/history", summary="Get all past triage records")
def get_history(db: Session = Depends(get_db)):
    """
    Returns all previously processed triage records ordered by newest first.
    """
    try:
        records = service.get_history(db)
        return ok([r.model_dump(mode="json") for r in records], f"{len(records)} records found.")
    except Exception as e:
        return server_error(str(e))
