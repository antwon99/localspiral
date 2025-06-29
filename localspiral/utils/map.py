"""Procedural generation for simple map layouts."""

from __future__ import annotations

import random
from typing import Iterable, Tuple


def generate_map(seed: int) -> list[list[str]]:
    """Return a deterministic 10x10 grid of tiles.

    Each tile is either ``'.'`` representing open ground or ``'#'`` for a wall.
    The layout is determined by the provided ``seed`` so that calling the
    function with the same seed always yields the same map.
    """
    rng = random.Random(seed)
    width = height = 10
    grid: list[list[str]] = []
    for _ in range(height):
        row = ['#' if rng.random() < 0.2 else '.' for _ in range(width)]
        grid.append(row)
    return grid


def with_player_marker(grid: Iterable[Iterable[str]], loc: Tuple[int, int]) -> list[list[str]]:
    """Return a copy of ``grid`` with ``'@'`` placed at ``loc``.

    The original grid is not modified.
    """
    new_grid = [list(row) for row in grid]
    r, c = loc
    if 0 <= r < len(new_grid) and 0 <= c < len(new_grid[0]):
        new_grid[r][c] = "@"
    return new_grid

