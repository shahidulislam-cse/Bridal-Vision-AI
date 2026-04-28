"""
config.py — BridalVision AI
============================
Centralized configuration using environment variables.
All sensitive keys (FAL_KEY) are loaded from .env — never hardcoded.

Author  : Shahidul Islam, Jr. AI Engineer
Company : Betopia Group / Join Venture AI, Dhaka, Bangladesh
"""

import os
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()


class Settings:
    """
    Application-wide settings loaded from environment variables.
    Add new config values here as the project grows.
    """

    # ── fal.ai ──────────────────────────────────────────────────
    FAL_KEY: str = os.getenv("FAL_KEY", "")
    FAL_MODEL: str = "fashn/tryon"          # IDM-VTON on fal.ai

    # ── Image Validation ─────────────────────────────────────────
    MAX_IMAGE_SIZE_MB: int = 5              # Maximum upload size (MB)
    ALLOWED_IMAGE_FORMATS: list[str] = [
        "JPEG",
        "PNG",
        "WEBP",
        "BMP",
        "TIFF",
        "GIF",
    ]

    # ── Session Limits ───────────────────────────────────────────
    MAX_TRYON_PER_SESSION: int = 3          # Brides get 3 try-ons max

    # ── API Timeout ──────────────────────────────────────────────
    FAL_TIMEOUT_SECONDS: int = 60           # Wait up to 60s for fal.ai

    # ── GDPR Note ────────────────────────────────────────────────
    # No user images are stored locally by the AI module.
    # Images are passed as URLs to fal.ai and result URLs are
    # returned to the backend. Storage/deletion is backend's responsibility.


# Single shared instance — import this everywhere
settings = Settings()