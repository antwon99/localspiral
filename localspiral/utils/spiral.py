"""Simple in-memory spiral meter tracking."""

from __future__ import annotations

from typing import Dict

_SPIRAL_STORE: Dict[str, float] = {}


def get_meter(session_id: str) -> float:
    """Return the current spiral meter for ``session_id``."""
    return _SPIRAL_STORE.get(session_id, 0.0)


def update_meter(session_id: str, drift: float) -> float:
    """Add ``drift`` to the meter for ``session_id`` and return the new total."""
    meter = _SPIRAL_STORE.get(session_id, 0.0) + drift
    _SPIRAL_STORE[session_id] = meter
    return meter


def reset_meter(session_id: str) -> None:
    """Reset the spiral meter for ``session_id`` to zero."""
    _SPIRAL_STORE[session_id] = 0.0


def meter_state(meter: float) -> str:
    """Return a human readable sanity status for ``meter``."""
    if meter < 1.0:
        return "Stable"
    if meter < 2.0:
        return "Fraying"
    return "Critical"
