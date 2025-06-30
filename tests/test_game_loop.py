from localspiral.utils.game_loop import apply_move, process_turn
from localspiral.utils.state import GameState
from localspiral.utils.enemies import Enemy
from localspiral.utils.zones import Zone
import copy


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


def test_process_turn_blocked_move(monkeypatch):
    grid = [["#", "#"], ["#", "."]]
    state = GameState(map_grid=grid, perceived_grid=[row[:] for row in grid], player_loc=(1, 1))

    monkeypatch.setattr("localspiral.utils.game_loop.generate_reply", lambda p, system_prompt=None: "ok")
    monkeypatch.setattr("localspiral.utils.game_loop.mutate_perceived_grid", lambda g, s: g)
    monkeypatch.setattr("localspiral.utils.game_loop.calculate_drift", lambda a, b: 0.0)
    monkeypatch.setattr("localspiral.utils.game_loop.check_keywords", lambda text, words=None: 0)
    monkeypatch.setattr("localspiral.utils.game_loop.distort_reply", lambda t, s, return_hallucination=False: (t, None))
    monkeypatch.setattr("localspiral.utils.game_loop.update_enemies", lambda s: None)
    monkeypatch.setattr("localspiral.utils.game_loop.add_enemy", lambda s: None)

    _, new_state = process_turn("move north", state)
    assert new_state.player_loc == (1, 1)


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
    assert reply.startswith("ok")
    assert new_state.player_loc == (1, 1)
    assert new_state.spiral_score >= 0


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


def test_history_truncation_keeps_pairs(monkeypatch):
    grid = [["." for _ in range(2)] for _ in range(2)]
    state = GameState(map_grid=grid, perceived_grid=[row[:] for row in grid])

    replies = ["r1", "r2", "r3", "r4"]

    def fake_reply(prompt, system_prompt=None):
        return replies.pop(0)

    monkeypatch.setattr("localspiral.utils.game_loop.generate_reply", fake_reply)
    monkeypatch.setattr("localspiral.utils.game_loop.mutate_perceived_grid", lambda g, s: g)
    monkeypatch.setattr("localspiral.utils.game_loop.calculate_drift", lambda a, b: 0.0)
    monkeypatch.setattr("localspiral.utils.game_loop.check_keywords", lambda text, words=None: 0)
    monkeypatch.setattr("localspiral.utils.game_loop.distort_reply", lambda t, s, return_hallucination=False: (t, None))
    monkeypatch.setattr("localspiral.utils.game_loop.update_enemies", lambda s: None)
    monkeypatch.setattr("localspiral.utils.game_loop.add_enemy", lambda s: None)

    prompts = ["p1", "p2", "p3", "p4"]
    for p in prompts:
        _, state = process_turn(p, state)

    assert state.history == ["r2", "p2", "r3", "p3", "r4", "p4"]


def test_door_hint_requires_visibility(monkeypatch):
    grid = [["." for _ in range(10)] for _ in range(10)]
    grid[5][6] = "#"
    grid[5][8] = "D"
    zone = Zone(name="Office", door_loc=(5, 8), start_loc=(5, 5), desk_loc=(5, 4))
    state = GameState(
        map_grid=copy.deepcopy(grid),
        perceived_grid=[row[:] for row in grid],
        player_loc=(5, 5),
        zones=[zone],
    )

    monkeypatch.setattr("localspiral.utils.game_loop.generate_reply", lambda p, system_prompt=None: "ok")
    monkeypatch.setattr("localspiral.utils.game_loop.mutate_perceived_grid", lambda g, s: g)
    monkeypatch.setattr("localspiral.utils.game_loop.calculate_drift", lambda a, b: 0.0)
    monkeypatch.setattr("localspiral.utils.game_loop.distort_reply", lambda t, s, return_hallucination=True: (t, None))
    monkeypatch.setattr("localspiral.utils.game_loop.update_enemies", lambda s: None)
    monkeypatch.setattr("localspiral.utils.game_loop.add_enemy", lambda s, **kw: None)

    reply, state = process_turn("look", state)
    assert "door" not in reply.lower()

    state.map_grid[5][6] = "."
    reply, state = process_turn("look", state)
    assert "door" in reply.lower()


def test_spammy_prompt_warning(monkeypatch):
    grid = [["." for _ in range(2)] for _ in range(2)]
    state = GameState(map_grid=grid, perceived_grid=[row[:] for row in grid])

    monkeypatch.setattr("localspiral.utils.game_loop.generate_reply", lambda p, system_prompt=None: "ignored")
    monkeypatch.setattr("localspiral.utils.game_loop.mutate_perceived_grid", lambda g, s: g)
    monkeypatch.setattr("localspiral.utils.game_loop.calculate_drift", lambda a, b: 0.0)
    monkeypatch.setattr("localspiral.utils.game_loop.distort_reply", lambda t, s, return_hallucination=True: (t, None))
    monkeypatch.setattr("localspiral.utils.game_loop.update_enemies", lambda s: None)
    monkeypatch.setattr("localspiral.utils.game_loop.add_enemy", lambda s, **kw: None)

    reply, _ = process_turn("coffee, your mother, science", state)
    assert "listing words" in reply.lower()
