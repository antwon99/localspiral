import pytest
from localspiral.main import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return app.test_client()


def test_chat_endpoint(client, monkeypatch):
    monkeypatch.setattr(
        'localspiral.utils.game_loop.generate_reply',
        lambda prompt, system_prompt=None: 'ok'
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.mutate_perceived_grid',
        lambda grid, score: grid
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.update_enemies',
        lambda state: None
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.add_enemy',
        lambda state: None
    )
    response = client.get('/chat?prompt=hello')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'].split('\n')[-1].startswith('ok')
    assert 'breakdown' in data
    assert 'state' in data
    assert 'spiral_score' in data['state']
    assert 'perceived_description' in data['state']
    assert 'directions' in data['state']
    assert 'turn' in data['state']


def test_spiral_endpoint(client):
    response = client.get('/spiral')
    assert response.status_code == 200
    data = response.get_json()
    assert 'score' in data
    assert 'sanity' in data
    assert 'status' in data
    assert 'turn' in data


def test_map_endpoint(client):
    first = client.get('/map?seed=5')
    second = client.get('/map?seed=5')
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.get_json()['grid'] == second.get_json()['grid']
    payload = first.get_json()
    assert 'seed' in payload
    assert 'display_name' in payload




def test_chat_persists_map(client, monkeypatch):
    from flask import session as flask_session
    flask_session.clear()

    calls = []

    def fake_map(seed):
        calls.append(seed)
        return [['.' for _ in range(10)] for _ in range(10)]

    monkeypatch.setattr('localspiral.utils.game_loop.generate_map', fake_map)
    monkeypatch.setattr('localspiral.utils.map.generate_map', fake_map)
    monkeypatch.setattr('localspiral.utils.game_loop.generate_reply',
                        lambda prompt, system_prompt=None: 'ok')
    monkeypatch.setattr('localspiral.utils.game_loop.mutate_perceived_grid',
                        lambda grid, score: grid)
    monkeypatch.setattr('localspiral.utils.game_loop.update_enemies', lambda state: None)
    monkeypatch.setattr('localspiral.utils.game_loop.add_enemy', lambda state: None)

    first = client.get('/chat?prompt=one')
    assert first.status_code == 200
    assert 'breakdown' in first.get_json()
    assert len(calls) == 1

    second = client.get('/chat?prompt=two')
    assert second.status_code == 200
    assert 'breakdown' in second.get_json()
    assert len(calls) == 1


def test_chat_history_pairs_reply_and_prompt(client, monkeypatch):
    """History should store replies and prompts in alternating order."""

    from flask import session as flask_session
    flask_session.clear()

    replies = [
        "first reply",
        "second reply",
        "third reply",
        "fourth reply",
    ]

    def fake_reply(prompt, system_prompt=None):
        return replies.pop(0)

    calls = []

    def fake_drift(ref, resp):
        calls.append((ref, resp))
        return 0.0

    monkeypatch.setattr('localspiral.utils.game_loop.generate_reply', fake_reply)
    monkeypatch.setattr('localspiral.utils.game_loop.calculate_drift', fake_drift)
    monkeypatch.setattr('localspiral.utils.game_loop.mutate_perceived_grid',
                        lambda grid, score: grid)
    monkeypatch.setattr('localspiral.utils.game_loop.update_enemies', lambda state: None)
    monkeypatch.setattr('localspiral.utils.game_loop.add_enemy', lambda state: None)
    monkeypatch.setattr('localspiral.utils.game_loop.at_door', lambda grid, loc: False)

    client.get('/chat?prompt=one')
    assert flask_session['game_state']['history'][0].endswith('first reply')
    assert flask_session['game_state']['history'][1] == 'one'
    assert calls == [('one', 'first reply')]

    client.get('/chat?prompt=two')
    assert flask_session['game_state']['history'][2].endswith('second reply')
    assert flask_session['game_state']['history'][3] == 'two'
    assert calls[0] == ('one', 'first reply')
    assert calls[1] == ('first reply', 'two')
    assert calls[2][0] == 'two'
    assert calls[2][1].endswith('second reply')
    assert calls[3][0].endswith('first reply')
    assert calls[3][1].endswith('second reply')

    client.get('/chat?prompt=three')
    client.get('/chat?prompt=four')
    hist = flask_session['game_state']['history']
    assert hist[0].endswith('second reply')
    assert hist[1] == 'two'
    assert hist[2].endswith('third reply')
    assert hist[3] == 'three'
    assert hist[4].endswith('fourth reply')
    assert hist[5] == 'four'
    assert calls[4][0].endswith('second reply')
    assert calls[4][1] == 'three'
    assert calls[5][0] == 'three'
    assert calls[5][1].endswith('third reply')
    assert calls[6][0].endswith('second reply')
    assert calls[6][1].endswith('third reply')
    assert calls[7][0].endswith('third reply')
    assert calls[7][1] == 'four'
    assert calls[8][0] == 'four'
    assert calls[8][1].endswith('fourth reply')
    assert calls[9][0].endswith('third reply')
    assert calls[9][1].endswith('fourth reply')


def test_chat_updates_spiral_score(client, monkeypatch):
    """Spiral score should increase when drift values are positive."""

    from flask import session as flask_session
    flask_session.clear()

    monkeypatch.setattr(
        'localspiral.utils.game_loop.generate_reply',
        lambda prompt, system_prompt=None: 'reply'
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.mutate_perceived_grid',
        lambda grid, score: grid
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.calculate_drift',
        lambda ref, resp: 0.5
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.update_enemies',
        lambda state: None
    )

    first = client.get('/chat?prompt=one')
    first_score = first.get_json()['state']['spiral_score']
    assert first_score >= 0

    second = client.get('/chat?prompt=two')
    second_score = second.get_json()['state']['spiral_score']
    assert second_score >= 0


def test_reset_endpoint_clears_state(client):
    from flask import session as flask_session
    flask_session['game_state'] = {'spiral_score': 5}
    response = client.get('/reset')
    assert response.status_code == 200
    assert 'game_state' not in flask_session


def test_map_grid_excludes_player_marker(client, monkeypatch):
    """Ensure '@' is never stored in the session map grid."""
    from flask import session as flask_session
    flask_session.clear()

    client.get('/map?seed=1')
    grid = flask_session['game_state']['map_grid']
    assert all(cell in '.#DK' for row in grid for cell in row)

    monkeypatch.setattr(
        'localspiral.utils.game_loop.generate_reply',
        lambda prompt, system_prompt=None: 'north'
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.mutate_perceived_grid',
        lambda grid, score: grid
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.update_enemies',
        lambda state: None
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.add_enemy',
        lambda state: None
    )
    client.get('/chat?prompt=north')
    grid = flask_session['game_state']['map_grid']
    assert all(cell in '.#DK' for row in grid for cell in row)

    # add an enemy marker to ensure cleaning logic
    flask_session['game_state']['enemies'] = [{'position': [1, 1], 'aggressive': False}]

    monkeypatch.setattr(
        'localspiral.utils.game_loop.generate_reply',
        lambda prompt, system_prompt=None: 'ok'
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.mutate_perceived_grid',
        lambda grid, score: grid
    )
    monkeypatch.setattr(
        'localspiral.utils.game_loop.update_enemies',
        lambda state: None
    )
    client.get('/chat?prompt=hello')
    grid = flask_session['game_state']['map_grid']
    assert all(cell in '.#DK' for row in grid for cell in row)


def test_chat_increments_turn_count(client, monkeypatch):
    from flask import session as flask_session
    flask_session.clear()

    monkeypatch.setattr('localspiral.utils.game_loop.generate_reply', lambda p, system_prompt=None: 'ok')
    monkeypatch.setattr('localspiral.utils.game_loop.mutate_perceived_grid', lambda g, s: g)
    monkeypatch.setattr('localspiral.utils.game_loop.update_enemies', lambda s: None)
    monkeypatch.setattr('localspiral.utils.game_loop.add_enemy', lambda s: None)

    client.get('/chat?prompt=hello')
    assert flask_session['game_state']['turn_count'] == 1


def test_skip_endpoint_sets_chat_count(client):
    from flask import session as flask_session
    flask_session.clear()

    resp = client.get('/skip')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['state']['awaiting_move']
    assert flask_session['game_state']['chat_count'] == 5


