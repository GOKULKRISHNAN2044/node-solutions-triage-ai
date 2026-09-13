from sqlalchemy.orm import Session
from repositories.schema.schema import TriageRecord


class TriageRepository:

    def save_triage(
        self,
        db: Session,
        raw_input: str,
        summary: str,
        category: str,
        priority: str,
        priority_reason: str,
        route: str,
        draft_response: str,
    ) -> TriageRecord:
        record = TriageRecord(
            raw_input=raw_input,
            summary=summary,
            category=category,
            priority=priority,
            priority_reason=priority_reason,
            route=route,
            draft_response=draft_response,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def get_all_triage(self, db: Session) -> list[TriageRecord]:
        return (
            db.query(TriageRecord)
            .order_by(TriageRecord.created_at.desc())
            .all()
        )

    def get_triage_by_id(self, db: Session, triage_id: int) -> TriageRecord | None:
        return db.query(TriageRecord).filter(TriageRecord.id == triage_id).first()
