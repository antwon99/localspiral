"""Procedural generation for simple map layouts."""

from __future__ import annotations

import random
from typing import Iterable, Tuple, Union
import hashlib


def compute_seed(value: Union[int, str]) -> int:
    """Return an ``int`` seed from ``value``.

    ``value`` may be an ``int`` or a ``str``. Strings are hashed so that
    identical inputs always yield the same integer.
    """
    if isinstance(value, int):
        return value
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]
    return int(digest, 16)


def generate_map(seed: Union[int, str], door_loc: Tuple[int, int] | None = None) -> list[list[str]]:
    """Return a deterministic 10x10 grid of tiles.

    Each tile is either ``'.'`` representing open ground or ``'#'`` for a wall.
    The layout is determined by ``seed`` so that calling the function with the
    same seed always yields the same map. If ``door_loc`` is provided a ``'D'``
    tile will be placed at that location.
    """
    rng = random.Random(compute_seed(seed))
    width = height = 10
    grid: list[list[str]] = []
    for _ in range(height):
        row = ['#' if rng.random() < 0.2 else '.' for _ in range(width)]
        grid.append(row)
    if door_loc:
        r, c = door_loc
        if 0 <= r < height and 0 <= c < width:
            grid[r][c] = 'D'
    return grid


def with_player_marker(
    grid: Iterable[Iterable[str]], loc: Tuple[int, int]
) -> list[list[str]]:
    """Return a copy of ``grid`` with ``'@'`` placed at ``loc``.

    The original grid is not modified.
    """
    new_grid = [list(row) for row in grid]
    r, c = loc
    if 0 <= r < len(new_grid) and 0 <= c < len(new_grid[0]):
        new_grid[r][c] = "@"
    return new_grid


def clean_entities(grid: Iterable[Iterable[str]] | None) -> list[list[str]] | None:
    """Return ``grid`` with player and enemy markers replaced by dots.

    ``None`` input is passed through unchanged.
    """
    if grid is None:
        return None
    cleaned = []
    for row in grid:
        cleaned.append([
            cell if cell not in {"@", "X"} else "."
            for cell in row
        ])
    return cleaned


def with_entities(
    grid: Iterable[Iterable[str]],
    player_loc: Tuple[int, int],
    enemies: Iterable[Tuple[int, int]] | None = None,
) -> list[list[str]]:
    """Return copy of ``grid`` with player and enemies marked."""
    new_grid = with_player_marker(grid, player_loc)
    if enemies:
        for r, c in enemies:
            if 0 <= r < len(new_grid) and 0 <= c < len(new_grid[0]):
                if new_grid[r][c] == ".":
                    new_grid[r][c] = "X"
    return new_grid
