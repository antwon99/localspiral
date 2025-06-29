# Expected: generate_map returns consistent size and stable output for same seed
from localspiral.utils.map_utils import generate_map, render_map


def test_generate_map_dimensions():
    grid = generate_map(width=5, height=4)
    assert len(grid) == 4
    assert all(len(row) == 5 for row in grid)


def test_generate_map_deterministic_seed():
    grid1 = generate_map(seed=42)
    grid2 = generate_map(seed=42)
    assert grid1 == grid2


def test_render_map_preserves_features():
    grid = generate_map(seed=99, width=5, height=5)
    rendered = render_map(grid, (2, 2))
    assert rendered[2][2] == "@"
    # All other tiles should match original grid
    for i in range(5):
        for j in range(5):
            if (i, j) != (2, 2):
                assert rendered[i][j] == grid[i][j]


def test_generate_map_contains_features_with_seed():
    grid = generate_map(seed=123, width=10, height=10)
    # At least one special tile should exist for deterministic seed
    specials = {"#", "!", "?"}
    assert any(cell in specials for row in grid for cell in row)
