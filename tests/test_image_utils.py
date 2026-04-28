"""
test_image_utils.py — BridalVision AI
=======================================
Unit tests for image validation utility.

Author  : Shahidul Islam, Jr. AI Engineer
Company : Betopia Group / Join Venture AI, Dhaka, Bangladesh
"""

import pytest
from io import BytesIO
from PIL import Image
from app.utils.image_utils import validate_image, ImageValidationError


def make_fake_image_bytes(format="JPEG") -> bytes:
    """Helper: create a real in-memory image as bytes."""
    img = Image.new("RGB", (100, 200), color=(255, 255, 255))
    buf = BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()


def test_valid_jpg_passes():
    """A valid JPG image should pass validation without error."""
    img_bytes = make_fake_image_bytes("JPEG")
    validate_image(img_bytes, "bride_photo.jpg")  # Should not raise


def test_valid_png_passes():
    """A valid PNG image should pass validation without error."""
    img_bytes = make_fake_image_bytes("PNG")
    validate_image(img_bytes, "bride_photo.png")  # Should not raise


def test_invalid_extension_raises():
    """A GIF file should raise ImageValidationError."""
    img_bytes = make_fake_image_bytes("JPEG")
    with pytest.raises(ImageValidationError, match="Invalid file type"):
        validate_image(img_bytes, "photo.gif")


def test_oversized_image_raises():
    """An image over 5MB should raise ImageValidationError."""
    large_bytes = b"0" * (6 * 1024 * 1024)  # 6MB of fake data
    with pytest.raises(ImageValidationError, match="too large"):
        validate_image(large_bytes, "big_photo.jpg")


def test_corrupted_image_raises():
    """Corrupted/non-image bytes should raise ImageValidationError."""
    fake_bytes = b"this is not an image at all"
    with pytest.raises(ImageValidationError, match="could not be read"):
        validate_image(fake_bytes, "photo.jpg")