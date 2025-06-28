"""Helpers for spiral scoring and narrative degradation."""
from __future__ import annotations

import random
from typing import Iterable, Tuple, Any


def spiral_status(score: float) -> str:
    """Return a status label for the given spiral score."""
    if score < 2:
        return "Lucid"
    if score < 4:
        return "Questioning"
    return "Erratic"


def distort_reply(reply: str, score: float) -> str:
    """Return a version of ``reply`` altered based on ``score``."""
    norm = min(score / 4.0, 1.0)
    if norm > 0.75 and random.random() < norm - 0.75:
        hallucinations = [
            "a door that isn't real",
            "shadowed figures",
            "flickering lights",
            "an impossible corridor",
        ]
        reply += f" I think I saw {random.choice(hallucinations)}..."
    if score < 2:
        return reply
    if score < 4:
        return f"{reply} ... I think."
    return f"{reply}\n{reply} I hear voices that weren't here before."


def analyze_map(grid: Iterable[Iterable[str]]) -> dict[str, Any]:
    """Return basic analysis of a map grid."""
    open_tiles = sum(row.count('.') for row in grid)
    wall_tiles = sum(row.count('#') for row in grid)
    if open_tiles > wall_tiles * 3:
        description = "mostly open corridors"
    elif wall_tiles > open_tiles:
        description = "claustrophobic maze"
    else:
        description = "balanced layout"
    return {
        "open": open_tiles,
        "walls": wall_tiles,
        "description": description,
    }


def describe_surroundings(grid: Iterable[Iterable[str]], loc: Tuple[int, int]) -> str:
    """Return a short description of tiles adjacent to ``loc``."""
    directions = {
        "north": (-1, 0),
        "south": (1, 0),
        "west": (0, -1),
        "east": (0, 1),
    }
    parts = []
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    for name, (dr, dc) in directions.items():
        r, c = loc[0] + dr, loc[1] + dc
        if 0 <= r < rows and 0 <= c < cols:
            tile = grid[r][c]
            if tile == '#':
                desc = 'wall'
            elif tile == '.':
                desc = 'corridor'
            elif tile == '@':
                desc = 'yourself'
            else:
                desc = 'void'
            parts.append(f"{name} {desc}")
    return ', '.join(parts)
