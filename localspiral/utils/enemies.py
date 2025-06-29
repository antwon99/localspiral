"""Basic enemy behaviors for the game loop."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .state import GameState

from .map import generate_map


@dataclass
class Enemy:
    """Simple enemy entity with optional patrol and hallucination flags."""

    position: Tuple[int, int]
    aggressive: bool = False
    patrol: List[Tuple[int, int]] | None = None
    hallucination: bool = False
    patrol_index: int = 0


def add_enemy(
    state: 'GameState',
    position: Tuple[int, int] | None = None,
    *,
    aggressive: bool = False,
    patrol: List[Tuple[int, int]] | None = None,
    hallucination: bool = False,
) -> Enemy:
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
                if all(
                    e.position != (r, c) for e in state.enemies
                ):
                    position = (r, c)
                    break
    enemy = Enemy(position, aggressive, patrol, hallucination)
    state.enemies.append(enemy)
    return enemy


def _random_move(enemy: Enemy, grid: List[List[str]]) -> None:
    r, c = enemy.position
    options = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    random.shuffle(options)
    for nr, nc in options:
        if (
            0 <= nr < len(grid)
            and 0 <= nc < len(grid[0])
            and grid[nr][nc] != '#'
        ):
            enemy.position = (nr, nc)
            break


def _chase_move(
    enemy: Enemy, grid: List[List[str]], target: Tuple[int, int]
) -> None:
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
        if (
            0 <= nr < len(grid)
            and 0 <= nc < len(grid[0])
            and grid[nr][nc] != '#'
        ):
            enemy.position = (nr, nc)
            break


def _patrol_move(enemy: Enemy, grid: List[List[str]]) -> None:
    """Move the enemy along its patrol route if possible."""
    if not enemy.patrol:
        _random_move(enemy, grid)
        return
    enemy.patrol_index = (enemy.patrol_index + 1) % len(enemy.patrol)
    nr, nc = enemy.patrol[enemy.patrol_index]
    if (
        0 <= nr < len(grid)
        and 0 <= nc < len(grid[0])
        and grid[nr][nc] != '#'
    ):
        enemy.position = (nr, nc)
    else:
        _random_move(enemy, grid)


def update_enemies(state: 'GameState') -> None:
    """Move all enemies one step."""
    grid = state.map_grid
    if grid is None:
        return

    for enemy in state.enemies:
        if enemy.aggressive:
            _chase_move(enemy, grid, state.player_loc)
        elif enemy.patrol:
            _patrol_move(enemy, grid)
        else:
            _random_move(enemy, grid)


def handle_enemy_encounters(state: 'GameState') -> str | None:
    """Update ``state`` if the player bumps into or nears an enemy.

    If the player occupies the same tile as an enemy ``state.spiral_score`` is
    increased by ``1``. When merely adjacent (including diagonals) the score is
    increased by ``0.5``. A short narrative snippet describing the encounter is
    returned or ``None`` if no enemies are near the player.
    """

    player_r, player_c = state.player_loc
    hall_close = [
        "A phantom whispers nonsense.",
        "A shadow blurs at the edge of vision.",
    ]
    hall_touch = [
        "The figure melts away as you collide.",
        "Your hand passes through a ghostly foe.",
    ]
    for enemy in state.enemies:
        er, ec = enemy.position
        if (er, ec) == (player_r, player_c):
            if enemy.hallucination:
                state.spiral_score += 1.5
                return random.choice(hall_touch)
            state.spiral_score += 1.0
            return "An enemy collides with you."
        if (
            abs(er - player_r) <= 1
            and abs(ec - player_c) <= 1
        ):
            if enemy.hallucination:
                state.spiral_score += 1.0
                return random.choice(hall_close)
            state.spiral_score += 0.5
            return "You feel an enemy lurking nearby."
    return None
