"""
endpoints.py — BridalVision AI
================================
FastAPI route definitions for the AI virtual try-on feature.

User uploads their photo directly as a file (not a URL).
The garment/dress is selected from the boutique's dress library (URL).

Available Endpoints:
  POST /api/tryon   — Upload photo + select dress → get try-on result
  GET  /api/health  — Check if AI service is running

Author  : Shahidul Islam, Jr. AI Engineer
Company : Betopia Group / Join Venture AI, Dhaka, Bangladesh
"""

import asyncio
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.fal_service import run_tryon
from app.utils.image_utils import validate_image, ImageValidationError, upload_image_to_fal

router = APIRouter()


# ─────────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────────

@router.get("/health")
def health_check():
    """
    Simple health check.
    Returns 200 OK if the AI service is running.
    """
    return {"status": "ok", "service": "BridalVision AI"}


# ─────────────────────────────────────────────
# Virtual Try-On Endpoint
# ─────────────────────────────────────────────

@router.post("/tryon")
async def tryon_endpoint(
    session_id        : str        = Form(...,  description="Unique session ID from backend"),
    garment_image_url : str        = Form(...,  description="URL of selected wedding dress from dress library"),
    dress_style       : str        = Form("default", description="Dress style: ball_gown | a_line | mermaid | sheath | lace | off_shoulder | default"),
    lighting          : str        = Form("default", description="Lighting: studio | outdoor | church | default"),
    human_image       : UploadFile = File(
        ...,
        description=(
            "Bride's full-body photo (JPG, PNG, WEBP, BMP, TIFF, GIF; "
            "no animations, max 5MB)"
        )
    ),
):
    """
    Run AI virtual bridal dress try-on.

    What the user sends:
      - human_image       : Their own photo uploaded directly as a file
      - garment_image_url : Dress URL selected from the boutique's collection
      - session_id        : To track the 3 try-on limit per session
      - dress_style       : Optional — for better prompt quality
      - lighting          : Optional — for better scene quality

    What comes back:
      - result_image_url  : AI-generated try-on image URL
      - tries_remaining   : How many try-ons are left in this session
      - message           : Status message
    """

    # ── Step 1: Read uploaded file bytes ─────────────────────────
    file_bytes = await human_image.read()
    filename   = human_image.filename or "upload.jpg"

    # ── Step 2: Validate the uploaded image ──────────────────────
    try:
        validate_image(file_bytes, filename)
    except ImageValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # ── Step 3: Upload image to fal.ai storage → get URL ─────────
    # fal.ai needs a URL — we upload the bytes and get a temporary URL back.
    # Run in a thread pool so the blocking network call doesn't stall
    # the FastAPI event loop.
    try:
        loop = asyncio.get_event_loop()
        human_image_url = await loop.run_in_executor(
            None, upload_image_to_fal, file_bytes, filename
        )
    except ImageValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload image for processing: {str(e)}"
        )

    # ── Step 4: Run AI try-on ─────────────────────────────────────
    result = run_tryon(
        human_image_url   = human_image_url,
        garment_image_url = garment_image_url,
        session_id        = session_id,
        dress_style       = dress_style,
        lighting          = lighting
    )

    # ── Step 5: Return result ─────────────────────────────────────
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])

    return result