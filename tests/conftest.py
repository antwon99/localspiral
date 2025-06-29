import pytest
from localspiral.main import app
from localspiral.utils.game_state import reset_game_state

@pytest.fixture()
def client():
    reset_game_state()
    with app.test_client() as client:
        yield client
    reset_game_state()
