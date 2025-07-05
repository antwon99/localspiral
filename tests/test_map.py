import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.map import GameMap
from game.player import Player


def test_map_borders_blocked():
    gm = GameMap(10, 10)
    assert all(tile == '#' for tile in gm.tiles[0])
    assert all(tile == '#' for tile in gm.tiles[-1])
    for row in gm.tiles:
        assert row[0] == '#'
        assert row[-1] == '#'


def test_player_moves_on_walkable_tiles():
    gm = GameMap(5, 5)
    player = Player(1, 1)
    moved = player.move(1, 0, gm)
    assert moved
    assert (player.x, player.y) == (2, 1)


def test_player_blocked_by_walls():
    gm = GameMap(5, 5)
    player = Player(1, 1)
    moved = player.move(-1, 0, gm)
    assert not moved
    assert (player.x, player.y) == (1, 1)
