from typing import List


def generate_map(seed: int = 0, width: int = 10, height: int = 10) -> List[List[str]]:
    """Return a stubbed map grid."""
    return [["." for _ in range(width)] for _ in range(height)]
