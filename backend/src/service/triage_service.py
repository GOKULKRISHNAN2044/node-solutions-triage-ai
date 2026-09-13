from sqlalchemy.orm import Session
from repositories.repo import TriageRepository
from service.gemini_service import analyze_request
from models.models import TriageResult


class TriageService:

    def __init__(self):
        self.repo = TriageRepository()

    def process_request(self, db: Session, request_text: str) -> TriageResult:
        """
        Orchestrates the full triage pipeline:
        1. Call Gemini to analyze the request
        2. Save the result to the database
        3. Return a TriageResult
        """
        ai_result = analyze_request(request_text)

        record = self.repo.save_triage(
            db=db,
            raw_input=request_text,
            summary=ai_result["summary"],
            category=ai_result["category"],
            priority=ai_result["priority"],
            priority_reason=ai_result["priority_reason"],
            route=ai_result["route"],
            draft_response=ai_result["draft_response"],
        )

        return TriageResult.model_validate(record)

    def get_history(self, db: Session) -> list[TriageResult]:
        """
        Fetches all past triage records ordered by newest first.
        """
        records = self.repo.get_all_triage(db)
        return [TriageResult.model_validate(r) for r in records]
