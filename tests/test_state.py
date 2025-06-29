import copy

from flask import session as flask_session

from localspiral.utils.state import GameState, save_game_state, load_game_state, CHARACTER_PATH
from localspiral.utils.characters import load_character


def test_save_game_state_cleans_grid():
    flask_session.clear()
    grid = [
        ['@', '.', 'X'],
        ['#', '@', '.'],
    ]
    state = GameState(map_grid=copy.deepcopy(grid))
    save_game_state(state)
    stored_grid = flask_session['game_state']['map_grid']
    assert all(cell in '.#' for row in stored_grid for cell in row)
    assert state.map_grid == stored_grid


def test_load_game_state_uses_tyler_profile():
    flask_session.clear()
    state = load_game_state()
    tyler = load_character(str(CHARACTER_PATH))
    assert state.character == tyler
    assert state.sanity == tyler.get('starting_sanity')


def test_save_load_round_trip_persists_fields():
    flask_session.clear()
    grid = [['.']]
    original = GameState(
        map_grid=copy.deepcopy(grid),
        player_loc=(3, 4),
        spiral_score=2.5,
        turn_count=7,
    )
    save_game_state(original)
    loaded = load_game_state()
    assert loaded.player_loc == (3, 4)
    assert loaded.spiral_score == 2.5
    assert loaded.turn_count == 7
    assert loaded.map_grid == [['.']]
