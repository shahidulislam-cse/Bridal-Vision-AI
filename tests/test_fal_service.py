"""
test_fal_service.py — BridalVision AI
=======================================
Unit tests for the fal_service AI wrapper.
Tests session limits and response formatting without real API calls.

Author  : Shahidul Islam, Jr. AI Engineer
Company : Betopia Group / Join Venture AI, Dhaka, Bangladesh
"""

import pytest
from unittest.mock import patch
from app.services.fal_service import run_tryon, format_response
from app.utils.session_utils import reset_session
from app.core import config as app_config


SESSION_ID = "test-session-001"
HUMAN_URL  = "https://example.com/bride.jpg"
DRESS_URL  = "https://example.com/dress.jpg"
MOCK_RESULT_URL = "https://fal.ai/results/mock-image.jpg"


@pytest.fixture(autouse=True)
def clear_session():
    """
    Reset session and inject a fake FAL_KEY before each test so that
    the early-exit guard in run_tryon() doesn't block our mocked calls.
    """
    original_key = app_config.settings.FAL_KEY
    app_config.settings.FAL_KEY = "test-fake-key-12345"
    reset_session(SESSION_ID)
    yield
    reset_session(SESSION_ID)
    app_config.settings.FAL_KEY = original_key


def test_session_limit_blocks_after_3_tryons():
    """After 3 successful try-ons, the 4th should be blocked."""

    mock_fal_response = {"images": [{"url": MOCK_RESULT_URL}]}

    with patch("app.services.fal_service.fal_client.run", return_value=mock_fal_response):
        # First 3 should succeed
        for i in range(3):
            result = run_tryon(HUMAN_URL, DRESS_URL, SESSION_ID)
            assert result["success"] is True, f"Try-on {i+1} should succeed"

        # 4th should be blocked
        result = run_tryon(HUMAN_URL, DRESS_URL, SESSION_ID)
        assert result["success"] is False
        assert result["tries_remaining"] == 0


def test_successful_tryon_returns_image_url():
    """A successful try-on should return the result image URL."""

    mock_fal_response = {"images": [{"url": MOCK_RESULT_URL}]}

    with patch("app.services.fal_service.fal_client.run", return_value=mock_fal_response):
        result = run_tryon(HUMAN_URL, DRESS_URL, SESSION_ID)

    assert result["success"] is True
    assert result["result_image_url"] == MOCK_RESULT_URL
    assert result["tries_remaining"] == 2


def test_format_response_structure():
    """format_response should always return required keys."""
    response = format_response(
        success=True,
        result_url=MOCK_RESULT_URL,
        session_id=SESSION_ID,
        message="Test message"
    )
    assert "success" in response
    assert "result_image_url" in response
    assert "tries_remaining" in response
    assert "message" in response


def test_missing_fal_key_returns_error():
    """If FAL_KEY is empty, run_tryon should return a clear error (no crash)."""
    original_key = app_config.settings.FAL_KEY
    app_config.settings.FAL_KEY = ""  # Simulate missing key
    try:
        result = run_tryon(HUMAN_URL, DRESS_URL, SESSION_ID)
        assert result["success"] is False
        assert "FAL_KEY" in result["message"]
    finally:
        app_config.settings.FAL_KEY = original_key