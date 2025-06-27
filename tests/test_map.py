import os

from localspiral.utils.map import generate_map


def test_generate_map_deterministic():
    map_a = generate_map(42)
    map_b = generate_map(42)
    assert map_a == map_b


def test_generate_map_different_seed():
    map_a = generate_map(1)
    map_b = generate_map(2)
    assert map_a != map_b
