"""Procedural generation for simple map layouts."""

from __future__ import annotations

import random


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
