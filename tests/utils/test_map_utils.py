# Expected: generate_map returns consistent size and stable output for same seed
from localspiral.utils.map_utils import generate_map


def test_generate_map_dimensions():
    grid = generate_map(width=5, height=4)
    assert len(grid) == 4
    assert all(len(row) == 5 for row in grid)


def test_generate_map_deterministic_seed():
    grid1 = generate_map(seed=42)
    grid2 = generate_map(seed=42)
    assert grid1 == grid2
