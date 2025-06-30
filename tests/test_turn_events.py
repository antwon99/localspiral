import copy

from localspiral.utils.game_loop import advance_state, process_turn
from localspiral.utils.enemies import Enemy
from localspiral.utils.state import GameState


def test_enemy_spawns_when_none():
    grid = [["." for _ in range(3)] for _ in range(3)]
    state = GameState(map_grid=copy.deepcopy(grid), player_loc=(1, 1))
    advance_state(state)
    assert state.enemies


def test_hallucination_spawn_every_five():
    grid = [["." for _ in range(3)] for _ in range(3)]
    state = GameState(map_grid=copy.deepcopy(grid), player_loc=(1, 1))
    state.turn_count = 5
    advance_state(state)
    assert any(e.hallucination for e in state.enemies)


def test_enemy_spawn_probability(monkeypatch):
    grid = [["." for _ in range(3)] for _ in range(3)]
    state = GameState(map_grid=copy.deepcopy(grid), player_loc=(1, 1))
    state.enemies.append(Enemy((2, 2)))
    monkeypatch.setattr(
        'localspiral.utils.game_loop.random.random',
        lambda: 0.1,
    )
    advance_state(state)
    assert len(state.enemies) == 2


def test_hallucination_spawn_every_five_forced(monkeypatch):
    grid = [["." for _ in range(3)] for _ in range(3)]
    state = GameState(map_grid=copy.deepcopy(grid), player_loc=(1, 1))
    state.turn_count = 5
    monkeypatch.setattr(
        'localspiral.utils.game_loop.random.random',
        lambda: 1.0,
    )
    advance_state(state)
    assert any(e.hallucination for e in state.enemies)


def test_baseline_decay(monkeypatch):
    grid = [["."]]
    state = GameState(
        map_grid=grid,
        perceived_grid=[row[:] for row in grid],
        spiral_score=0.5,
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.generate_reply',
        lambda p, system_prompt=None: 'ok',
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.mutate_perceived_grid',
        lambda g, s: g,
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.calculate_drift',
        lambda a, b: 0.0,
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.check_keywords',
        lambda text, words=None: 0,
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.distort_reply',
        lambda t, s, return_hallucination=True: (t, None),
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.update_enemies',
        lambda s: None,
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.add_enemy',
        lambda s, **kw: None,
    )
    _, new_state = process_turn('wait', state)
    assert new_state.spiral_score < 0.5
