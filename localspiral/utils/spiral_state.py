"""Helpers for spiral state and map awareness."""
from __future__ import annotations

import random
from typing import Iterable, Tuple, Any

TRIGGER_WORDS = {
    "real",
    "door",
    "kill",
    "escape",
    "loop",
    "who",
    "are",
    "you",
}


def check_keywords(text: str) -> int:
    """Return the number of trigger words present in ``text``."""
    lowered = text.lower()
    return sum(1 for w in TRIGGER_WORDS if w in lowered)


def spiral_status(score: float) -> str:
    """Return a short status label for the given spiral score."""
    if score < 2:
        return "Lucid"
    if score < 4:
        return "Questioning"
    return "Erratic"


def distort_reply(text: str, score: float) -> str:
    """Warp ``text`` slightly based on ``score``."""
    if score >= 8:
        text += " [The map warps and glitches before your eyes]"
        text = text.upper()
    elif score >= 6:
        hallucinations = [
            "a door that isn't real",
            "shadowed figures",
            "flickering lights",
            "echoing footsteps that stop abruptly",
        ]
        text += " I can't stop seeing " + random.choice(hallucinations) + "!"
        text = text.upper()
    elif score >= 4:
        hallucinations = [
            "a door that isn't real",
            "shadowed figures",
            "flickering lights",
        ]
        text += " I think I saw " + random.choice(hallucinations) + "..."
    elif score >= 2:
        text += " ... I think."
    return text


def analyze_map(grid: Iterable[Iterable[str]]) -> dict[str, Any]:
    """Return a basic description of ``grid``."""
    open_tiles = sum(row.count('.') for row in grid)
    wall_tiles = sum(row.count('#') for row in grid)
    desc = "balanced layout"
    if open_tiles > wall_tiles * 3:
        desc = "mostly open corridors"
    elif wall_tiles > open_tiles:
        desc = "claustrophobic maze"
    return {"open": open_tiles, "walls": wall_tiles, "description": desc}


def describe_surroundings(grid: Iterable[Iterable[str]], loc: Tuple[int, int]) -> str:
    """Return short text describing tiles next to ``loc``."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    parts: list[str] = []
    for name, (dr, dc) in {
        "north": (-1, 0),
        "south": (1, 0),
        "west": (0, -1),
        "east": (0, 1),
    }.items():
        r, c = loc[0] + dr, loc[1] + dc
        if 0 <= r < rows and 0 <= c < cols:
            tile = grid[r][c]
            if tile == '#':
                desc = 'wall'
            elif tile == '.':
                desc = 'corridor'
            else:
                desc = 'void'
            parts.append(f"{name} {desc}")
    return ', '.join(parts)
