from localspiral.utils.game_loop import apply_move, process_turn
from localspiral.utils.state import GameState
from localspiral.utils.enemies import Enemy


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


def test_recovery_anchor_reduces_spiral(monkeypatch):
    grid = [[".", "."]]
    character = {
        "display_name": "Tyler",
        "starting_sanity": 100,
        "spiral_triggers": [],
        "recovery_anchors": ["coffee"],
        "tone": "test",
        "intro_prompt": "intro",
    }
    state = GameState(
        map_grid=grid,
        perceived_grid=[row[:] for row in grid],
        spiral_score=1.0,
        paranoia_level=1.0,
        character=character,
    )

    monkeypatch.setattr("localspiral.utils.game_loop.generate_reply", lambda p, system_prompt=None: "ok")
    monkeypatch.setattr("localspiral.utils.game_loop.mutate_perceived_grid", lambda g, s: g)
    monkeypatch.setattr("localspiral.utils.game_loop.calculate_drift", lambda a, b: 0.0)

    def fake_check(text, words=None):
        if words == character["recovery_anchors"]:
            return 1
        return 0

    monkeypatch.setattr("localspiral.utils.game_loop.check_keywords", fake_check)
    monkeypatch.setattr("localspiral.utils.game_loop.distort_reply", lambda t, s, return_hallucination=False: (t, None))
    monkeypatch.setattr("localspiral.utils.game_loop.update_enemies", lambda s: None)
    monkeypatch.setattr("localspiral.utils.game_loop.add_enemy", lambda s: None)

    _, new_state = process_turn("sip some coffee", state)
    assert new_state.spiral_score < 1.0
    assert new_state.paranoia_level < 1.0


def test_process_turn_enemy_encounter(monkeypatch):
    grid = [["." for _ in range(2)] for _ in range(2)]
    enemy = Enemy((0, 1))
    state = GameState(
        map_grid=grid,
        perceived_grid=[row[:] for row in grid],
        player_loc=(0, 0),
        enemies=[enemy],
    )

    monkeypatch.setattr("localspiral.utils.game_loop.generate_reply", lambda p, system_prompt=None: "ok")
    monkeypatch.setattr("localspiral.utils.game_loop.mutate_perceived_grid", lambda g, s: g)
    monkeypatch.setattr("localspiral.utils.game_loop.calculate_drift", lambda a, b: 0.0)
    monkeypatch.setattr("localspiral.utils.game_loop.check_keywords", lambda text, words=None: 0)
    monkeypatch.setattr("localspiral.utils.game_loop.distort_reply", lambda t, s, return_hallucination=False: (t, None))
    monkeypatch.setattr("localspiral.utils.game_loop.update_enemies", lambda s: None)
    monkeypatch.setattr("localspiral.utils.game_loop.add_enemy", lambda s: None)

    _, new_state = process_turn("wait", state)
    assert new_state.spiral_score > 0
