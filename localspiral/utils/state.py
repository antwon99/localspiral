"""Helpers for storing and retrieving game state from the session."""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
import random
from flask import session
from typing import List, Tuple
from pathlib import Path

from .characters import load_character

CHARACTER_PATH = Path(__file__).resolve().parents[1] / "characters" / "tyler.json"


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
    character: dict | None = None
    last_hallucination: str | None = None
    paranoia_level: float = 0.0

    def update_sanity(self) -> None:
        """Recalculate sanity based on the current spiral score."""
        base = 100
        if self.character and isinstance(self.character, dict):
            base = self.character.get("starting_sanity", 100)
        self.sanity = max(0, base - int(self.spiral_score * 20))


def load_game_state() -> GameState:
    """Return :class:`GameState` instance from the session."""
    data = session.get("game_state")
    if not isinstance(data, dict):
        character = load_character(str(CHARACTER_PATH))
        return GameState(character=character)
        return GameState(
            character=character,
            sanity=character.get("starting_sanity", 100),
        )
    character = data.get("character")
    if character is None:
        character = load_character(str(CHARACTER_PATH))
    return GameState(
        spiral_score=data.get("spiral_score", 0.0),
        sanity=data.get("sanity", character.get("starting_sanity", 100)),
        map_grid=data.get("map_grid"),
        map_seed=data.get("map_seed", random.randint(0, 2**32 - 1)),
        player_loc=tuple(data.get("player_loc", (5, 5))),
        perceived_grid=data.get("perceived_grid"),
        history=list(data.get("history", [])),
        character=character,
        last_hallucination=data.get("last_hallucination"),
        paranoia_level=data.get("paranoia_level", 0.0),
    )


def save_game_state(state: GameState) -> None:
    """Persist ``state`` to the session."""
    session["game_state"] = asdict(state)
