"""Simple zone management utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from . import map as map_utils
from .map import compute_seed


@dataclass
class Zone:
    """Representation of a world zone."""

    name: str
    door_loc: Tuple[int, int] = (9, 5)
    start_loc: Tuple[int, int] = (5, 5)


TYLER_ZONES = [
    "Office",
    "Hallway",
    "Stairs",
    "Street",
    "Bus",
    "Home",
]


def get_zones_for_character(character_id: str) -> List[Zone]:
    """Return zone list for ``character_id``."""
    if character_id == "tyler":
        return [Zone(name=n) for n in TYLER_ZONES]
    # Fallback single zone
    return [Zone(name="Start")]


def get_zone_seed(base_seed: int, zone: Zone, index: int) -> int:
    """Return deterministic seed for a zone."""
    token = f"zone_{index}_{zone.name.lower()}_{base_seed}"
    return compute_seed(token)


def ensure_zone_map(base_seed: int, zone: Zone, index: int) -> List[List[str]]:
    """Generate map for ``zone`` using ``base_seed``."""
    seed = get_zone_seed(base_seed, zone, index)
    grid = map_utils.generate_map(seed)
    r, c = zone.door_loc
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
        grid[r][c] = 'D'
    return grid


def at_door(grid: List[List[str]], loc: Tuple[int, int]) -> bool:
    """Return True if ``loc`` is a door tile in ``grid``."""
    r, c = loc
    return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == "D"


def should_leave_zone(text: str, zone: Zone) -> bool:
    """Return True if ``text`` implies leaving the current ``zone``."""
    lower = text.lower()
    return "leave zone" in lower or f"leave {zone.name.lower()}" in lower


def move_to_next_zone(state) -> str | None:
    """Advance ``state`` to the next zone if available."""
    zones = getattr(state, "zones", [])
    index = getattr(state, "zone_index", 0)
    if index >= len(zones) - 1:
        return None
    previous = zones[index]
    state.zone_index = index + 1
    next_zone = zones[state.zone_index]
    state.map_grid = ensure_zone_map(state.map_seed, next_zone, state.zone_index)
    state.player_loc = next_zone.start_loc
    return f"You leave {previous.name} and enter {next_zone.name}."
