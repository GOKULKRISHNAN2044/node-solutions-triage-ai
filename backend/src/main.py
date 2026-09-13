import sys
from pathlib import Path

# Ensure src/ directory is always in Python's module search path
_src_dir = str(Path(__file__).resolve().parent)
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from repositories.database import Base, engine, SessionLocal
from repositories.user_repo import UserRepository
from router.router import router
from settings import config

import uvicorn

# Create all DB tables on startup and ensure default admin exists
Base.metadata.create_all(bind=engine)
with SessionLocal() as _startup_db:
    UserRepository().seed_default_admin(_startup_db)

app = FastAPI(
    title=config.app_title,
    description="AI-powered request triage assistant — classifies, prioritizes, routes, and drafts responses for incoming business requests.",
    version=config.app_version,
)

# Allow all origins so local and deployed frontends (e.g. Vercel) can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "app": config.app_title, "version": config.app_version}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
