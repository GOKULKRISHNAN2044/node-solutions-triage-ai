from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

# Always load .env from the same directory as this file (src/)
load_dotenv(dotenv_path=Path(__file__).parent / ".env")


@dataclass
class Config:
    gemini_api_key: str
    db_url: str
    app_title: str
    app_version: str


def get_config() -> Config:
    return Config(
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        db_url=os.getenv("DB_URL", "sqlite:///./triage.db"),
        app_title="Node Solutions — AI Request Triage Assistant",
        app_version="1.0.0",
    )


config = get_config()
