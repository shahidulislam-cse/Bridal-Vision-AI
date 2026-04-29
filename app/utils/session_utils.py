"""
session_utils.py — BridalVision AI
=====================================
Tracks how many AI try-ons a bride has used in a single session.
Maximum allowed: 3 try-ons per session (as per project requirement).

Note:
  This is a lightweight in-memory store.
  For production, the backend dev should replace this with
  Redis or a database-backed session store.

Author  : Shahidul Islam, Jr. AI Engineer
Company : Betopia Group / Join Venture AI, Dhaka, Bangladesh
"""

from app.core.config import settings
import threading

# ─────────────────────────────────────────────
# In-memory session store
# Format: { "session_id_string": try_on_count }
# NOTE: For multi-worker deployments, replace with Redis.
# ─────────────────────────────────────────────
_session_store: dict[str, int] = {}
_lock = threading.Lock()  # Thread-safe for single-worker uvicorn


def get_tryon_count(session_id: str) -> int:
    """
    Return how many try-ons the current session has used.

    Args:
        session_id (str): Unique session ID provided by the backend.

    Returns:
        int: Number of try-ons used (0 if session is new).
    """
    return _session_store.get(session_id, 0)


def can_tryon(session_id: str) -> bool:
    """
    Check whether the session is still within the try-on limit.

    Args:
        session_id (str): Unique session ID provided by the backend.

    Returns:
        bool: True if try-on is allowed, False if limit is reached.
    """
    with _lock:
        count = _session_store.get(session_id, 0)
    return count < settings.MAX_TRYON_PER_SESSION


def increment_tryon_count(session_id: str) -> int:
    """
    Increment the try-on count for a session after a successful try-on.
    Thread-safe via lock.

    Args:
        session_id (str): Unique session ID provided by the backend.

    Returns:
        int: Updated try-on count after incrementing.
    """
    with _lock:
        current = _session_store.get(session_id, 0)
        _session_store[session_id] = current + 1
        return _session_store[session_id]


def get_remaining_tryons(session_id: str) -> int:
    """
    Return how many try-ons the bride has left in this session.

    Args:
        session_id (str): Unique session ID provided by the backend.

    Returns:
        int: Remaining try-ons (min 0).
    """
    used = get_tryon_count(session_id)
    remaining = settings.MAX_TRYON_PER_SESSION - used
    return max(remaining, 0)


def reset_session(session_id: str) -> None:
    """
    Reset the try-on count for a session (useful for testing).

    Args:
        session_id (str): Unique session ID to reset.
    """
    if session_id in _session_store:
        del _session_store[session_id]