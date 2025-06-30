"""Helpers for spiral state and map awareness."""
from __future__ import annotations

import random
from typing import Iterable, Tuple, Any, Dict

# Default trigger words used when a character profile does not specify any.
DEFAULT_TRIGGER_WORDS = {
    "shit",
    "fuck",
    "die",
    "death",
    "run",
    "kill",
    "escape",
}

# Direction offsets used when analyzing the map. Only the
# four primary directions are considered for movement.
DIRECTION_VECTORS: Dict[str, Tuple[int, int]] = {
    "north": (-1, 0),
    "south": (1, 0),
    "west": (0, -1),
    "east": (0, 1),
}


def check_keywords(
    text: str, trigger_words: Iterable[str] | None = None
) -> int:
    """Return the number of trigger words present in ``text``.

    Parameters
    ----------
    text:
        The user supplied text to scan.
    trigger_words:
        Optional collection of trigger words. If ``None`` the
        :data:`DEFAULT_TRIGGER_WORDS` set is used.
    """

    lowered = text.lower()
    words = trigger_words or DEFAULT_TRIGGER_WORDS
    return sum(1 for w in words if w in lowered)


def spiral_status(score: float) -> str:
    """Return a short status label for the given spiral score."""
    if score < 2:
        return "Lucid"
    if score < 4:
        return "Questioning"
    return "Erratic"


def distort_reply(
    text: str, score: float, *, return_hallucination: bool = False
) -> str | tuple[str, str | None]:
    """Warp ``text`` slightly based on ``score``.

    Optionally return the hallucination used.
    """
    hallucination: str | None = None
    if score >= 8:
        hallucination = "the map warping and glitching"
        text += " [The map warps and glitches before your eyes]"
        text = text.upper()
    elif score >= 6:
        hallucinations = [
            "a door that isn't real",
            "shadowed figures",
            "flickering lights",
            "echoing footsteps that stop abruptly",
        ]
        hallucination = random.choice(hallucinations)
        text += " I can't stop seeing " + hallucination + "!"
        text = text.upper()
    elif score >= 5:
        hallucinations = [
            "a door that isn't real",
            "Gernon Security",
            "shadowed figures",
            "flickering lights",
            "echoing footsteps",
        ]
        hallucination = random.choice(hallucinations)
        text += " I think I saw " + hallucination + "..."
        hallucination = random.choice(hallucinations)
        text += " I can't stop seeing " + hallucination + "!"
        text = text.upper()
    elif score >= 4:
        hallucinations = [
            "a door that isn't real",
            "shadowed figures",
            "flickering lights",
        ]
        hallucination = random.choice(hallucinations)
        fragment = random.choice(text.split())
        text += " I think I saw " + hallucination + "... " + fragment + "..."
    elif score >= 2:
        text += " ... I think."
    if return_hallucination:
        return text, hallucination
    return text


def mutate_perceived_grid(
    grid: list[list[str]], score: float
) -> list[list[str]]:
    """Return a hallucinated version of ``grid`` based on ``score``."""
    if score < 5 or not grid:
        return [row[:] for row in grid]

    chance = 0.1
    if score >= 8:
        chance = 0.3

    new_grid = [row[:] for row in grid]
    for r, row in enumerate(new_grid):
        for c, _ in enumerate(row):
            if random.random() < chance:
                new_grid[r][c] = '?'
    return new_grid


def analyze_map(grid: Iterable[Iterable[str]]) -> dict[str, Any]:
    """Return a basic description of ``grid``."""
    open_tiles = sum(row.count('.') for row in grid)
    wall_tiles = sum(row.count('#') for row in grid)
    desc = "balanced layout"
    if open_tiles > wall_tiles * 3:
        desc = "mostly open corridors"
    elif wall_tiles > open_tiles:
        desc = "claustrophobic maze"
    return {
        "open": open_tiles,
        "walls": wall_tiles,
        "description": desc,
    }


def get_available_directions(
    grid: Iterable[Iterable[str]], loc: Tuple[int, int]
) -> list[str]:
    """Return a list of directions the player can move to from ``loc``."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    available: list[str] = []
    for name, (dr, dc) in DIRECTION_VECTORS.items():
        r, c = loc[0] + dr, loc[1] + dc
        if 0 <= r < rows and 0 <= c < cols and grid[r][c] != "#":
            available.append(name)
    return available


def describe_surroundings(
    grid: Iterable[Iterable[str]], loc: Tuple[int, int]
) -> str:
    """Return short text describing tiles next to ``loc``."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    parts: list[str] = []
    for name, (dr, dc) in DIRECTION_VECTORS.items():
        r, c = loc[0] + dr, loc[1] + dc
        if 0 <= r < rows and 0 <= c < cols:
            tile = grid[r][c]
            if tile == '#':
                desc = 'wall'
            elif tile == '.':
                desc = 'corridor'
            elif tile == 'D':
                desc = 'door'
            elif tile == 'K':
                desc = 'desk'
            else:
                desc = 'void'
            parts.append(f"{name} {desc}")
    return ', '.join(parts)


def describe_location(
    grid: Iterable[Iterable[str]], loc: Tuple[int, int]
) -> str:
    """Return a short description of the tile under ``loc``."""

    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    r, c = loc
    if not (0 <= r < rows and 0 <= c < cols):
        return "void"

    tile = grid[r][c]
    if tile == "#":
        return "wall"
    if tile == ".":
        return "corridor"
    if tile == "@":
        return "player"
    if tile == "?":
        return "distortion"
    if tile == "D":
        return "door"
    if tile == "K":
        return "desk"
    return "void"
