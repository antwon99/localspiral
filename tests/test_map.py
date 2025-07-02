from localspiral.utils.map import generate_map, clean_entities, clean_enemies


def test_generate_map_deterministic():
    map_a = generate_map(42)
    map_b = generate_map(42)
    assert map_a == map_b


def test_generate_map_different_seed():
    map_a = generate_map(1)
    map_b = generate_map(2)
    assert map_a != map_b


def test_clean_entities_replaces_markers():
    grid = [
        ["@", ".", "X"],
        ["#", "X", "@"],
    ]
    cleaned = clean_entities(grid)
    assert cleaned == [
        [".", ".", "."],
        ["#", ".", "."],
    ]


def test_clean_entities_none():
    assert clean_entities(None) is None


def test_clean_enemies_preserves_player():
    grid = [
        ["@", "X"],
        ["X", "."],
    ]
    cleaned = clean_enemies(grid)
    assert cleaned == [
        ["@", "."],
        [".", "."],
    ]
