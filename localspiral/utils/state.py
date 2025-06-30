"""Helpers for storing and retrieving game state from the session."""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
import random
from flask import session
from typing import List, Tuple
from pathlib import Path

from .enemies import Enemy

from .characters import load_character
from .zones import Zone, get_zones_for_character, ensure_zone_map

CHARACTER_PATH = (
    Path(__file__).resolve().parents[1] / "characters" / "tyler.json"
)


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
    turn_count: int = 0
    character: dict | None = None
    last_hallucination: str | None = None
    paranoia_level: float = 0.0
    enemies: List[Enemy] = field(default_factory=list)
    zone_index: int = 0
    zones: List = field(default_factory=list)

    def update_sanity(self) -> None:
        """Recalculate sanity based on the current spiral score."""
        base = 100
        if self.character and isinstance(self.character, dict):
            base = self.character.get("starting_sanity", 100)
        self.sanity = max(0, base - int(self.spiral_score * 20))


def _clean_grid(grid: List[List[str]] | None) -> List[List[str]] | None:
    """Return ``grid`` with any entity markers removed."""
    if grid is None:
        return None
    cleaned = []
    for row in grid:
        cleaned.append([
            '.' if cell in {'@', 'X', 'D'} else cell
            for cell in row
        ])
    return cleaned


def load_game_state() -> GameState:
    """Return :class:`GameState` instance from the session."""
    data = session.get("game_state")
    if not isinstance(data, dict):
        character = load_character(str(CHARACTER_PATH))
        zones = get_zones_for_character(character.get("id", "tyler"))
        base_seed = random.randint(0, 2**32 - 1)
        return GameState(character=character, zones=zones, map_seed=base_seed)
    character = data.get("character")
    if character is None:
        character = load_character(str(CHARACTER_PATH))
    enemies = [
        Enemy(tuple(e.get("position", (0, 0))), e.get("aggressive", False))
        for e in data.get("enemies", [])
        if isinstance(e, dict)
    ]
    return GameState(
        spiral_score=data.get("spiral_score", 0.0),
        sanity=data.get("sanity", character.get("starting_sanity", 100)),
        map_grid=_clean_grid(data.get("map_grid")),
        map_seed=data.get("map_seed", random.randint(0, 2**32 - 1)),
        player_loc=tuple(data.get("player_loc", (5, 5))),
        perceived_grid=data.get("perceived_grid"),
        history=list(data.get("history", [])),
        turn_count=data.get("turn_count", 0),
        character=character,
        last_hallucination=data.get("last_hallucination"),
        paranoia_level=data.get("paranoia_level", 0.0),
        enemies=enemies,
        zone_index=data.get("zone_index", 0),
        zones=[Zone(name=z['name'], door_loc=tuple(z['door_loc']), start_loc=tuple(z['start_loc'])) if isinstance(z, dict) else z for z in data.get("zones", get_zones_for_character(character.get("id", "tyler")))],
    )


def save_game_state(state: GameState) -> None:
    """Persist ``state`` to the session."""
    state.map_grid = _clean_grid(state.map_grid)
    session["game_state"] = asdict(state)
