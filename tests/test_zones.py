import copy
from localspiral.utils.zones import Zone, ensure_zone_map, move_to_next_zone
from localspiral.utils.state import GameState


def test_ensure_zone_map_start_open(monkeypatch):
    grid = [
        ['.', '.', '.'],
        ['.', '#', '.'],
        ['.', '.', '.'],
    ]

    def fake_map(seed):
        return [row[:] for row in grid]

    zone = Zone(name="Test", start_loc=(1, 1))
    monkeypatch.setattr('localspiral.utils.zones.map_utils.generate_map', fake_map)
    result = ensure_zone_map(1, zone, 0)
    r, c = zone.start_loc
    assert result[r][c] != '#'
    assert zone.start_loc != (1, 1)


def test_move_to_next_zone_resets_position(monkeypatch):
    grid = [
        ['.', '.', '.'],
        ['.', '#', '.'],
        ['.', '.', '.'],
    ]

    def fake_map(seed):
        return [row[:] for row in grid]

    zone1 = Zone(name="A")
    zone2 = Zone(name="B", start_loc=(1, 1))
    monkeypatch.setattr('localspiral.utils.zones.map_utils.generate_map', fake_map)
    state = GameState(zones=[zone1, zone2], map_seed=1)
    state.map_grid = ensure_zone_map(state.map_seed, zone1, 0)
    msg = move_to_next_zone(state)
    assert msg is not None
    assert state.player_loc == zone2.start_loc
    r, c = state.player_loc
    assert state.map_grid[r][c] != '#'

