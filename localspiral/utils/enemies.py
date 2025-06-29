"""Basic enemy behaviors for the game loop."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Tuple

from .map import generate_map


@dataclass
class Enemy:
    """Simple enemy entity."""

    position: Tuple[int, int]
    aggressive: bool = False


def add_enemy(state: 'GameState', position: Tuple[int, int] | None = None, *, aggressive: bool = False) -> Enemy:
    """Add a new enemy to ``state`` at ``position`` or a random open tile."""
    grid = state.map_grid
    if grid is None:
        grid = generate_map(state.map_seed)
        state.map_grid = grid

    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    rng = random.Random()

    if position is None:
        while True:
            r = rng.randint(0, rows - 1)
            c = rng.randint(0, cols - 1)
            if grid[r][c] == '.' and (r, c) != state.player_loc:
                if all(e.position != (r, c) for e in state.enemies):
                    position = (r, c)
                    break
    enemy = Enemy(position, aggressive)
    state.enemies.append(enemy)
    return enemy


def _random_move(enemy: Enemy, grid: List[List[str]]) -> None:
    r, c = enemy.position
    options = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    random.shuffle(options)
    for nr, nc in options:
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            enemy.position = (nr, nc)
            break


def _chase_move(enemy: Enemy, grid: List[List[str]], target: Tuple[int, int]) -> None:
    r, c = enemy.position
    pr, pc = target
    candidates: List[Tuple[int, int]] = []
    if pr > r:
        candidates.append((r + 1, c))
    elif pr < r:
        candidates.append((r - 1, c))
    if pc > c:
        candidates.append((r, c + 1))
    elif pc < c:
        candidates.append((r, c - 1))
    if not candidates:
        candidates = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    random.shuffle(candidates)
    for nr, nc in candidates:
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            enemy.position = (nr, nc)
            break


def update_enemies(state: 'GameState') -> None:
    """Move all enemies one step."""
    grid = state.map_grid
    if grid is None:
        return

    for enemy in state.enemies:
        if enemy.aggressive:
            _chase_move(enemy, grid, state.player_loc)
        else:
            _random_move(enemy, grid)
