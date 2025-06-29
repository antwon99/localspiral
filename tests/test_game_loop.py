from localspiral.utils.game_loop import apply_move, process_turn
from localspiral.utils.state import GameState


def test_apply_move_succeeds():
    grid = [[".", "."], [".", "."]]
    state = GameState(map_grid=grid, player_loc=(1, 0))
    moved = apply_move(state, "east")
    assert moved
    assert state.player_loc == (1, 1)


def test_apply_move_blocked():
    grid = [["#", "#"], [".", "."]]
    state = GameState(map_grid=grid, player_loc=(1, 1))
    moved = apply_move(state, "north")
    assert not moved
    assert state.player_loc == (1, 1)


def test_process_turn_updates_state(monkeypatch):
    grid = [[".", "."], [".", "."]]
    state = GameState(map_grid=grid, perceived_grid=[row[:] for row in grid], player_loc=(1, 0))

    monkeypatch.setattr("localspiral.utils.game_loop.generate_reply", lambda prompt, system_prompt=None: "ok")
    monkeypatch.setattr("localspiral.utils.game_loop.mutate_perceived_grid", lambda g, s: g)
    monkeypatch.setattr("localspiral.utils.game_loop.calculate_drift", lambda a, b: 0.5)
    monkeypatch.setattr("localspiral.utils.game_loop.check_keywords", lambda text, words=None: 0)
    monkeypatch.setattr("localspiral.utils.game_loop.distort_reply", lambda t, s, return_hallucination=False: (t, None))
    monkeypatch.setattr("localspiral.utils.game_loop.update_enemies", lambda s: None)
    monkeypatch.setattr("localspiral.utils.game_loop.add_enemy", lambda s: None)

    reply, new_state = process_turn("go east", state)
    assert reply == "ok"
    assert new_state.player_loc == (1, 1)
    assert new_state.spiral_score > 0


def test_process_turn_increments_turn_count(monkeypatch):
    grid = [[".", "."], [".", "."]]
    state = GameState(map_grid=grid, perceived_grid=[row[:] for row in grid])

    monkeypatch.setattr("localspiral.utils.game_loop.generate_reply", lambda p, system_prompt=None: "ok")
    monkeypatch.setattr("localspiral.utils.game_loop.mutate_perceived_grid", lambda g, s: g)
    monkeypatch.setattr("localspiral.utils.game_loop.calculate_drift", lambda a, b: 0.0)
    monkeypatch.setattr("localspiral.utils.game_loop.check_keywords", lambda text, words=None: 0)
    monkeypatch.setattr("localspiral.utils.game_loop.distort_reply", lambda t, s, return_hallucination=False: (t, None))
    monkeypatch.setattr("localspiral.utils.game_loop.update_enemies", lambda s: None)
    monkeypatch.setattr("localspiral.utils.game_loop.add_enemy", lambda s: None)

    assert state.turn_count == 0
    _, new_state = process_turn("east", state)
    assert new_state.turn_count == 1
