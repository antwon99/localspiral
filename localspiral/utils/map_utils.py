from typing import List, Tuple, Optional
import random


def generate_map(seed: int = 0, width: int = 10, height: int = 10) -> List[List[str]]:
    """Generate a simple deterministic map.

    A ``random.Random`` instance seeded with ``seed`` controls placement of
    obstacles and interactive tiles. ``#`` represents an obstacle, ``!`` an
    interactive feature and ``.`` open ground.
    """
    rng = random.Random(seed)
    grid: List[List[str]] = []
    for _ in range(height):
        row: List[str] = []
        for _ in range(width):
            roll = rng.random()
            if roll < 0.1:
                row.append("#")
            elif roll < 0.15:
                row.append("!")
            elif roll < 0.2:
                row.append("?")
            else:
                row.append(".")
        grid.append(row)
    return grid


def parse_direction(prompt: str) -> Optional[str]:
    """Return cardinal direction found in the prompt if any."""
    prompt = prompt.lower()
    for direction in ["north", "south", "east", "west"]:
        if direction in prompt:
            return direction
    return None


def move_position(
    position: Tuple[int, int], direction: str, grid: List[List[str]]
) -> Tuple[Tuple[int, int], bool]:
    """Move the position within the grid if possible."""
    x, y = position
    height, width = len(grid), len(grid[0])
    deltas = {
        "north": (-1, 0),
        "south": (1, 0),
        "west": (0, -1),
        "east": (0, 1),
    }
    dx, dy = deltas.get(direction, (0, 0))
    nx, ny = x + dx, y + dy
    if 0 <= nx < height and 0 <= ny < width:
        return (nx, ny), True
    return position, False


def render_map(grid: List[List[str]], position: Tuple[int, int]) -> List[List[str]]:
    """Return a map grid with the player symbol placed."""
    rendered = [row[:] for row in grid]
    x, y = position
    if 0 <= x < len(rendered) and 0 <= y < len(rendered[0]):
        rendered[x][y] = "@"
    return rendered
