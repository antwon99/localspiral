from __future__ import annotations

"""Helpers for storing and retrieving game state from the session."""

from dataclasses import dataclass, asdict, field
import random
from flask import session
from typing import List, Tuple


@dataclass
class GameState:
    """Simple container for all persistent game values."""

    spiral_score: float = 0.0
    sanity: int = 100
    map_grid: List[List[str]] | None = None
    perceived_grid: List[List[str]] | None = None
    map_seed: int = field(default_factory=lambda: random.randint(0, 2**32 - 1))
    player_loc: Tuple[int, int] = (5, 5)
    history: List[str] = field(default_factory=list)

    def update_sanity(self) -> None:
        """Recalculate sanity based on the current spiral score."""
        self.sanity = max(0, 100 - int(self.spiral_score * 20))


def load_game_state() -> GameState:
    """Return :class:`GameState` instance from the session."""
    data = session.get("game_state")
    if not isinstance(data, dict):
        return GameState()
    return GameState(
        spiral_score=data.get("spiral_score", 0.0),
        sanity=data.get("sanity", 100),
        map_grid=data.get("map_grid"),
        map_seed=data.get("map_seed", random.randint(0, 2**32 - 1)),
        player_loc=tuple(data.get("player_loc", (5, 5))),
        perceived_grid=data.get("perceived_grid"),
        history=list(data.get("history", [])),
    )


def save_game_state(state: GameState) -> None:
    """Persist ``state`` to the session."""
    session["game_state"] = asdict(state)
