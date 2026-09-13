from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from repositories.database import Base, engine
from router.router import router
from settings import config

import uvicorn

# Create all DB tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=config.app_title,
    description="AI-powered request triage assistant — classifies, prioritizes, routes, and drafts responses for incoming business requests.",
    version=config.app_version,
)

# Allow React dev server to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
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
