from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import config

Base = declarative_base()


class Database:
    def __init__(self):
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
        )

    def _create_engine(self):
        return create_engine(
            config.db_url,
            connect_args={"check_same_thread": False},  # required for SQLite
        )


_db_instance = Database()
engine = _db_instance.engine
SessionLocal = _db_instance.SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
