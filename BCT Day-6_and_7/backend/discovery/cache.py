"""
cache.py – In-memory LRU-style cache for recent scan results.

Prevents redundant re-scans of hosts that were just discovered.
TTL defaults to 5 minutes.
"""
import time
from typing import Optional, Dict, Tuple

_CACHE: Dict[str, Tuple[dict, float]] = {}
DEFAULT_TTL = 300  # seconds


def get(key: str) -> Optional[dict]:
    """Return cached scan result if not expired, else None."""
    if key in _CACHE:
        data, ts = _CACHE[key]
        if time.time() - ts < DEFAULT_TTL:
            return data
        del _CACHE[key]
    return None


def set(key: str, value: dict, ttl: int = DEFAULT_TTL):
    """Cache a scan result."""
    _CACHE[key] = (value, time.time())


def invalidate(key: str):
    """Remove a specific key from the cache."""
    _CACHE.pop(key, None)


def clear():
    """Flush the entire cache."""
    _CACHE.clear()


def size() -> int:
    return len(_CACHE)
