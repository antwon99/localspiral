from localspiral.utils.game_state import GameState
from localspiral.utils.spiral import update_spiral


def test_update_spiral_changes_tone_at_threshold():
    state = GameState()
    state.spiral = 24
    update_spiral(state, "", "")
    assert state.spiral == 25
    assert state.character["tone"] == "tense"


def test_update_spiral_triggers_hallucination_at_final_threshold():
    state = GameState()
    state.spiral = 74
    update_spiral(state, "", "")
    assert state.spiral == 75
    assert state.hallucinating is True
    assert state.character["tone"] == "hallucinatory"
