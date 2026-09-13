from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from repositories.database import Base


class TriageRecord(Base):
    __tablename__ = "triage_records"

    id = Column(Integer, primary_key=True, index=True)
    raw_input = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    priority = Column(String(20), nullable=False)
    priority_reason = Column(Text, nullable=False)
    route = Column(String(100), nullable=False)
    draft_response = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
