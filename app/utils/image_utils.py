"""
image_utils.py - BridalVision AI
================================
Handles photo upload validation and preprocessing.

User uploads their photo directly as a file.
After validation, the image bytes are uploaded to fal.ai
temporary storage to get a URL which IDM-VTON requires.

Flow:
  user uploads file
  -> validate_image() checks size/format/corruption
  -> upload_image_to_fal() uploads bytes -> returns temp URL

GDPR note:
  Images are validated in memory only.
  fal.ai temporary storage auto-deletes after processing.
  Nothing is saved to local disk by this module.
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
# Format helpers
# ─────────────────────────────────────────────

FORMAT_TO_MIME = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "WEBP": "image/webp",
    "BMP": "image/bmp",
    "TIFF": "image/tiff",
    "GIF": "image/gif",
}


def _inspect_image(file_bytes: bytes) -> tuple[Image.Image, str, bool]:
    """
    Open and validate image bytes, returning a usable Image and metadata.

    Returns:
        tuple: (Image, format_str, is_animated)
    """
    try:
        img = Image.open(io.BytesIO(file_bytes))
        img.verify()
    except Exception:
        raise ImageValidationError(
            "Your photo could not be read. "
            "Please upload a valid image file."
        )

    img = Image.open(io.BytesIO(file_bytes))
    img.load()

    image_format = (img.format or "").upper()
    is_animated = bool(getattr(img, "is_animated", False)) and getattr(img, "n_frames", 1) > 1

    return img, image_format, is_animated


def _validate_format(image_format: str, is_animated: bool) -> None:
    if not image_format or image_format not in settings.ALLOWED_IMAGE_FORMATS:
        allowed = ", ".join(settings.ALLOWED_IMAGE_FORMATS)
        raise ImageValidationError(
            f"Unsupported image format '{image_format or 'unknown'}'. "
            f"Supported formats: {allowed}."
        )

    if is_animated:
        raise ImageValidationError(
            "Animated images are not supported. "
            "Please upload a still photo."
        )


def _convert_to_png_bytes(img: Image.Image) -> bytes:
    if img.mode in ("RGBA", "LA") or "transparency" in img.info:
        img = img.convert("RGBA")
    else:
        img = img.convert("RGB")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ─────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────

def validate_image(file_bytes: bytes, filename: str) -> None:
    """
    Validate the uploaded image file.

    Checks:
      1. File size is under MAX_IMAGE_SIZE_MB
      2. File is a real image (not corrupted or fake)
      3. File format is supported
      4. Image is not animated

    Args:
        file_bytes (bytes): Raw bytes of the uploaded file.
        filename   (str)  : Original filename (used for messages only).

    Raises:
        ImageValidationError: With a clear message if any check fails.
    """

    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > settings.MAX_IMAGE_SIZE_MB:
        raise ImageValidationError(
            f"Photo is too large ({size_mb:.1f}MB). "
            f"Maximum allowed size is {settings.MAX_IMAGE_SIZE_MB}MB."
        )

    img, image_format, is_animated = _inspect_image(file_bytes)
    _validate_format(image_format, is_animated)


# ─────────────────────────────────────────────
# fal.ai Image Upload
# ─────────────────────────────────────────────

def upload_image_to_fal(file_bytes: bytes, filename: str) -> str:
    """
    Upload image bytes to fal.ai temporary storage.

    IDM-VTON requires an image URL. fal.ai provides a built-in upload
    function that stores the image temporarily and returns a public URL.

    For non-JPEG/PNG formats, the image is converted to PNG before upload.

    Args:
        file_bytes (bytes): Raw bytes of the validated image.
        filename   (str)  : Original filename (unused, kept for API parity).

    Returns:
        str: Temporary fal.ai URL for the uploaded image.

    Raises:
        ImageValidationError: If the image is invalid or unsupported.
        Exception: If upload to fal.ai fails.
    """

    img, image_format, is_animated = _inspect_image(file_bytes)
    _validate_format(image_format, is_animated)

    if image_format in ("JPEG", "PNG"):
        upload_bytes = file_bytes
        content_type = FORMAT_TO_MIME[image_format]
    else:
        upload_bytes = _convert_to_png_bytes(img)
        content_type = FORMAT_TO_MIME["PNG"]

    size_mb = len(upload_bytes) / (1024 * 1024)
    if size_mb > settings.MAX_IMAGE_SIZE_MB:
        raise ImageValidationError(
            f"Photo is too large after conversion ({size_mb:.1f}MB). "
            f"Maximum allowed size is {settings.MAX_IMAGE_SIZE_MB}MB."
        )

    image_url = fal_client.upload(
        data=upload_bytes,
        content_type=content_type
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