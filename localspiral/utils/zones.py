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
    desk_loc: Tuple[int, int] | None = None


TYLER_ZONES = [
    Zone(name="Office", door_loc=(5, 8), start_loc=(5, 5), desk_loc=(5, 4)),
    Zone(name="Hallway"),
    Zone(name="Stairs"),
    Zone(name="Street"),
    Zone(name="Bus"),
    Zone(name="Home"),
]


def get_zones_for_character(character_id: str) -> List[Zone]:
    """Return zone list for ``character_id``."""
    if character_id == "tyler":
        return [
            Zone(
                name=z.name,
                door_loc=z.door_loc,
                start_loc=z.start_loc,
                desk_loc=z.desk_loc,
            )
            for z in TYLER_ZONES
        ]
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
    if zone.desk_loc:
        dr, dc = zone.desk_loc
        if 0 <= dr < len(grid) and 0 <= dc < len(grid[0]):
            grid[dr][dc] = 'K'
    return grid


def door_visible(
    grid: List[List[str]],
    door_loc: Tuple[int, int],
    player_loc: Tuple[int, int],
    max_range: int = 3,
) -> bool:
    """Return ``True`` if the door can be reached within ``max_range`` steps."""

    from collections import deque

    if not grid:
        return False
    rows = len(grid)
    cols = len(grid[0])
    if not (0 <= door_loc[0] < rows and 0 <= door_loc[1] < cols):
        return False

    q = deque([(player_loc, 0)])
    visited = {player_loc}

    while q:
        (r, c), dist = q.popleft()
        if dist > max_range:
            continue
        if (r, c) == door_loc:
            return True
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and grid[nr][nc] != '#'
                and (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                q.append(((nr, nc), dist + 1))
    return False


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
