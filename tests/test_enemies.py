from localspiral.utils.enemies import add_enemy, update_enemies, Enemy
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
