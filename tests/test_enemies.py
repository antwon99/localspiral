from localspiral.utils.enemies import (
    add_enemy,
    update_enemies,
    Enemy,
    handle_enemy_encounters,
)
from localspiral.utils.state import GameState


def test_add_enemy_places_enemy():
    grid = [["." for _ in range(3)] for _ in range(3)]
    state = GameState(map_grid=grid, player_loc=(1, 1))
    enemy = add_enemy(state, position=(0, 0))
    assert enemy in state.enemies
    assert enemy.position == (0, 0)


def test_update_enemies_moves_toward_player(monkeypatch):
    grid = [["." for _ in range(3)] for _ in range(3)]
    state = GameState(map_grid=grid, player_loc=(2, 2))
    enemy = Enemy((0, 0), aggressive=True)
    state.enemies.append(enemy)
    monkeypatch.setattr('localspiral.utils.enemies.random.shuffle', lambda x: None)
    update_enemies(state)
    assert enemy.position in {(1, 0), (0, 1)}


def test_handle_enemy_encounters_collision():
    grid = [["." for _ in range(2)] for _ in range(2)]
    enemy = Enemy((0, 0))
    state = GameState(map_grid=grid, player_loc=(0, 0), enemies=[enemy])
    snippet = handle_enemy_encounters(state)
    assert snippet is not None
    assert state.spiral_score == 1.0


def test_handle_enemy_encounters_adjacent():
    grid = [["." for _ in range(2)] for _ in range(2)]
    enemy = Enemy((0, 1))
    state = GameState(map_grid=grid, player_loc=(0, 0), enemies=[enemy])
    snippet = handle_enemy_encounters(state)
    assert snippet is not None
    assert state.spiral_score == 0.5
