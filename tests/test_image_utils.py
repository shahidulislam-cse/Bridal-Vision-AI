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


def make_fake_image_bytes(format="JPEG", **save_kwargs) -> bytes:
    """Helper: create a real in-memory image as bytes."""
    img = Image.new("RGB", (100, 200), color=(255, 255, 255))
    buf = BytesIO()
    img.save(buf, format=format, **save_kwargs)
    return buf.getvalue()


def make_animated_gif_bytes() -> bytes:
    """Helper: create a small animated GIF as bytes."""
    frames = [
        Image.new("RGB", (64, 64), color=(255, 255, 255)),
        Image.new("RGB", (64, 64), color=(200, 200, 200)),
    ]
    buf = BytesIO()
    frames[0].save(
        buf,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=100,
    )
    return buf.getvalue()


def test_valid_jpg_passes():
    """A valid JPG image should pass validation without error."""
    img_bytes = make_fake_image_bytes("JPEG")
    validate_image(img_bytes, "bride_photo.jpg")  # Should not raise


def test_valid_png_passes():
    """A valid PNG image should pass validation without error."""
    img_bytes = make_fake_image_bytes("PNG")
    validate_image(img_bytes, "bride_photo.png")  # Should not raise


def test_animated_gif_raises():
    """Animated GIFs should raise ImageValidationError."""
    img_bytes = make_animated_gif_bytes()
    with pytest.raises(ImageValidationError, match="Animated images are not supported"):
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