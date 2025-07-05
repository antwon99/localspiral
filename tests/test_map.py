import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.map import GameMap


def test_map_borders_blocked():
    gm = GameMap(10, 10)
    assert all(tile == '#' for tile in gm.tiles[0])
    assert all(tile == '#' for tile in gm.tiles[-1])
    for row in gm.tiles:
        assert row[0] == '#'
        assert row[-1] == '#'
