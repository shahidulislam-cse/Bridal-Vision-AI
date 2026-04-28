"""
fal_service.py — BridalVision AI
===================================
Main AI service wrapper for the virtual bridal dress try-on feature.

This module integrates with fal.ai using the IDM-VTON model.
It is the core of the AI developer's responsibility in this project.

Responsibilities:
  - Call fal.ai IDM-VTON with user photo + dress image
  - Enforce session try-on limits (max 3 per session)
  - Validate input images before sending to API
  - Handle timeouts and API errors gracefully
  - Return clean, formatted JSON responses to the backend

GDPR Compliance:
  - No user images are stored locally by this module
  - Images are passed as URLs; result URLs are returned to backend
  - Backend is responsible for storage, deletion, and data policies

Author  : Shahidul Islam, Jr. AI Engineer
Company : Betopia Group / Join Venture AI, Dhaka, Bangladesh
"""

import os
import time
import fal_client
from app.core.config import settings
from app.core.prompts import build_tryon_prompt
from app.utils.session_utils import can_tryon, increment_tryon_count, get_remaining_tryons


# ─────────────────────────────────────────────
# Set fal.ai API key from environment
# ─────────────────────────────────────────────
os.environ["FAL_KEY"] = settings.FAL_KEY


# ─────────────────────────────────────────────
# Core Functions
# ─────────────────────────────────────────────

def run_tryon(
    human_image_url: str,
    garment_image_url: str,
    session_id: str,
    dress_style: str = "default",
    lighting: str = "default"
) -> dict:
    """
    Run the AI virtual dress try-on using fal.ai IDM-VTON model.

    Steps:
      1. Check session try-on limit
      2. Call fal.ai with human photo + garment image
      3. Retry once on timeout
      4. Return formatted result

    Args:
        human_image_url   (str): URL of the bride's full-body photo.
        garment_image_url (str): URL of the selected wedding dress image.
        session_id        (str): Session ID from backend (used for limit tracking).
        dress_style       (str): Optional dress style to improve prompt quality.
        lighting          (str): Optional lighting scene to improve prompt quality.

    Returns:
        dict: {
            "success"         : bool,
            "result_image_url" : str | None,
            "tries_remaining" : int,
            "message"         : str
        }
    """

    # ── Step 1: Check Session Limit ──────────────────────────────
    if not can_tryon(session_id):
        return format_response(
            success=False,
            result_url=None,
            session_id=session_id,
            message=(
                f"You have reached the maximum of "
                f"{settings.MAX_TRYON_PER_SESSION} try-ons for this session. "
                f"Please book an appointment to try more dresses in store!"
            )
        )

    if not settings.FAL_KEY:
        return format_response(
            success=False,
            result_url=None,
            session_id=session_id,
            message="FAL_KEY is missing. Set it in the environment before running."
        )

    prompts = build_tryon_prompt(dress_style=dress_style, lighting=lighting)

    # ── Step 2: Call fal.ai (with one retry on failure) ──────────
    fal_result = _call_fal_with_retry(
        human_image_url,
        garment_image_url,
        prompt=prompts["positive"],
        negative_prompt=prompts["negative"]
    )

    if not fal_result["success"]:
        return format_response(
            success=False,
            result_url=None,
            session_id=session_id,
            message=fal_result["error"]
        )

    # ── Step 3: Increment session count on success ────────────────
    increment_tryon_count(session_id)

    return format_response(
        success=True,
        result_url=fal_result["image_url"],
        session_id=session_id,
        message="Your virtual try-on is ready! ✨"
    )


def _call_fal_with_retry(
    human_image_url: str,
    garment_image_url: str,
    prompt: str,
    negative_prompt: str,
    retries: int = 1
) -> dict:
    """
    Internal function: call fal.ai IDM-VTON and retry once on failure.

    Args:
        human_image_url   (str): URL of the bride's photo.
        garment_image_url (str): URL of the wedding dress image.
        prompt            (str): Positive prompt for IDM-VTON.
        negative_prompt   (str): Negative prompt for IDM-VTON.
        retries           (int): Number of retry attempts (default: 1).

    Returns:
        dict: {"success": bool, "image_url": str | None, "error": str | None}
    """

    attempt = 0
    last_error = ""

    while attempt <= retries:
        try:
            # ── Call fal.ai IDM-VTON ─────────────────────────────
            result = fal_client.run(
                settings.FAL_MODEL,
                arguments={
                    "human_image_url"  : human_image_url,
                    "garment_image_url": garment_image_url,
                    "prompt"           : prompt,
                    "negative_prompt"  : negative_prompt,
                    "num_inference_steps": 30,
                    "guidance_scale"   : 2.0,
                }
            )

            # ── Extract result image URL ──────────────────────────
            image_url = _extract_image_url(result)

            if image_url:
                return {"success": True, "image_url": image_url, "error": None}
            else:
                last_error = "fal.ai returned a result but no image URL was found."

        except Exception as e:
            last_error = str(e)
            if attempt < retries:
                time.sleep(2)  # Short pause before retry

        attempt += 1

    return {
        "success"  : False,
        "image_url": None,
        "error"    : f"AI service failed after {retries + 1} attempt(s): {last_error}"
    }


def _extract_image_url(fal_result: dict) -> str | None:
    """
    Extract the result image URL from fal.ai's response object.

    fal.ai IDM-VTON returns: { "images": [{"url": "..."}] }

    Args:
        fal_result (dict): Raw response from fal.ai.

    Returns:
        str | None: Image URL if found, else None.
    """
    try:
        return fal_result["images"][0]["url"]
    except (KeyError, IndexError, TypeError):
        return None


def format_response(
    success: bool,
    result_url: str | None,
    session_id: str,
    message: str
) -> dict:
    """
    Format a clean, consistent JSON response for the backend.

    Args:
        success    (bool)      : Whether the try-on was successful.
        result_url (str|None)  : URL of the generated try-on image.
        session_id (str)       : Session ID (used to get remaining count).
        message    (str)       : Human-readable status message.

    Returns:
        dict: Standardized response object.
    """
    return {
        "success"         : success,
        "result_image_url": result_url,
        "tries_remaining" : get_remaining_tryons(session_id),
        "message"         : message
    }