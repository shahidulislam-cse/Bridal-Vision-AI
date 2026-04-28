"""
main.py — BridalVision AI
===========================
FastAPI application entry point.
The backend developer imports and mounts this app into their Django setup.

Run locally:
    uvicorn main:app --reload --port 8001

Author  : Shahidul Islam, Jr. AI Engineer
Company : Betopia Group / Join Venture AI, Dhaka, Bangladesh
"""

from fastapi import FastAPI
from app.api.endpoints import router

# ── Create FastAPI app ────────────────────────────────────────────
app = FastAPI(
    title       = "BridalVision AI",
    description = "AI-powered virtual bridal dress try-on service using fal.ai IDM-VTON",
    version     = "1.0.0"
)

# ── Register API routes under /api prefix ─────────────────────────
app.include_router(router, prefix="/api")


# ── Root endpoint (optional) ──────────────────────────────────────
@app.get("/")
def root():
    return {
        "project": "BridalVision AI",
        "status" : "running",
        "docs"   : "/docs"
    }