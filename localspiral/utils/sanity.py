from __future__ import annotations

from .game_state import GameState


DEFAULT_SANITY_CAP = 100


def change_sanity(state: GameState, amount: int) -> None:
    """Modify sanity within the 0 - DEFAULT_SANITY_CAP range."""
    cap = state.character.get("starting_sanity", DEFAULT_SANITY_CAP)
    state.sanity = max(0, min(state.sanity + amount, cap))


def adjust_sanity_from_spiral(state: GameState, increment: int) -> None:
    """Decrease sanity in proportion to spiral gain."""
    if increment > 0:
        change_sanity(state, -increment)
