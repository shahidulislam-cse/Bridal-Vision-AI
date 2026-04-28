"""
image_utils.py — BridalVision AI
==================================
Handles photo upload validation and preprocessing.

User uploads their photo directly as a file (JPG/PNG).
After validation, the image bytes are uploaded to fal.ai
temporary storage to get a URL — which IDM-VTON needs.

Flow:
  User uploads file
      → validate_image()       checks format, size, corruption
      → upload_image_to_fal()  uploads bytes → returns temp URL
      → fal_service.py         sends URL to IDM-VTON

GDPR Note:
  Images are validated in memory only.
  fal.ai temporary storage auto-deletes after processing.
  Nothing is saved to local disk by this module.

Author  : Shahidul Islam, Jr. AI Engineer
Company : Betopia Group / Join Venture AI, Dhaka, Bangladesh
"""

import io
import fal_client
from PIL import Image
from app.core.config import settings


# ─────────────────────────────────────────────
# Custom Exception
# ─────────────────────────────────────────────

class ImageValidationError(Exception):
    """Raised when an uploaded image fails validation."""
    pass


# ─────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────

def validate_image(file_bytes: bytes, filename: str) -> None:
    """
    Validate the uploaded image file.

    Checks:
      1. File extension is JPG or PNG
      2. File size is under MAX_IMAGE_SIZE_MB (5MB)
      3. File is a real image (not corrupted or fake)

    Args:
        file_bytes (bytes): Raw bytes of the uploaded file.
        filename   (str)  : Original filename for extension check.

    Raises:
        ImageValidationError: With a clear message if any check fails.
    """

    # ── Check 1: File Extension ──────────────────────────────────
    extension = filename.rsplit(".", 1)[-1].lower()
    if extension not in settings.ALLOWED_EXTENSIONS:
        raise ImageValidationError(
            f"Invalid file type '.{extension}'. "
            f"Please upload a JPG or PNG photo."
        )

    # ── Check 2: File Size ───────────────────────────────────────
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > settings.MAX_IMAGE_SIZE_MB:
        raise ImageValidationError(
            f"Photo is too large ({size_mb:.1f}MB). "
            f"Maximum allowed size is {settings.MAX_IMAGE_SIZE_MB}MB."
        )

    # ── Check 3: Real Image (not corrupted) ──────────────────────
    try:
        img = Image.open(io.BytesIO(file_bytes))
        img.verify()
    except Exception:
        raise ImageValidationError(
            "Your photo could not be read. "
            "Please upload a valid JPG or PNG image."
        )


# ─────────────────────────────────────────────
# fal.ai Image Upload
# ─────────────────────────────────────────────

def upload_image_to_fal(file_bytes: bytes, filename: str) -> str:
    """
    Upload image bytes to fal.ai temporary storage.

    IDM-VTON model requires an image URL — not raw bytes.
    fal.ai provides a built-in upload function that:
      - Takes raw bytes
      - Stores them temporarily
      - Returns a public URL usable by IDM-VTON

    The temporary URL auto-expires after processing.
    No permanent storage occurs.

    Args:
        file_bytes (bytes): Raw bytes of the validated image.
        filename   (str)  : Original filename (used for content-type detection).

    Returns:
        str: Temporary fal.ai URL for the uploaded image.

    Raises:
        Exception: If upload to fal.ai fails.
    """

    # ── Detect content type from extension ───────────────────────
    extension    = filename.rsplit(".", 1)[-1].lower()
    content_type = "image/jpeg" if extension in ["jpg", "jpeg"] else "image/png"

    # ── Upload to fal.ai storage ──────────────────────────────────
    # fal_client.upload() returns a public temporary URL
    image_url = fal_client.upload(
        data         = file_bytes,
        content_type = content_type
    )

    return image_url


# ─────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────

def get_image_dimensions(file_bytes: bytes) -> dict:
    """
    Return image width and height in pixels.

    Args:
        file_bytes (bytes): Raw image bytes.

    Returns:
        dict: {"width": int, "height": int}
    """
    img = Image.open(io.BytesIO(file_bytes))
    width, height = img.size
    return {"width": width, "height": height}