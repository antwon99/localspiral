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
        'localspiral.routes.chat.generate_reply',
        lambda prompt, system_prompt=None: 'ok'
    )
    monkeypatch.setattr(
        'localspiral.routes.chat.mutate_perceived_grid',
        lambda grid, score: grid
    )
    response = client.get('/chat?prompt=hello')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'ok'
    assert 'breakdown' in data
    assert 'state' in data
    assert 'spiral_score' in data['state']
    assert 'perceived_description' in data['state']
    assert 'directions' in data['state']


def test_spiral_endpoint(client):
    response = client.get('/spiral')
    assert response.status_code == 200
    data = response.get_json()
    assert 'score' in data
    assert 'sanity' in data
    assert 'status' in data


def test_map_endpoint(client):
    first = client.get('/map?seed=5')
    second = client.get('/map?seed=5')
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.get_json()['grid'] == second.get_json()['grid']
    payload = first.get_json()
    assert 'seed' in payload
    assert 'display_name' in payload


def test_move_endpoint(client, monkeypatch):
    from flask import session as flask_session
    flask_session.clear()

    grid = [['.' for _ in range(10)] for _ in range(10)]

    def fake_map(seed):
        return [row[:] for row in grid]

    monkeypatch.setattr('localspiral.routes.map.generate_map', fake_map)
    monkeypatch.setattr('localspiral.routes.move.generate_map', fake_map)

    client.get('/map?seed=1')
    resp = client.get('/move?dir=north')
    assert resp.status_code == 200
    data = resp.get_json()
    assert tuple(data['location']) == (4, 5)
    assert 'directions' in data


def test_chat_persists_map(client, monkeypatch):
    from flask import session as flask_session
    flask_session.clear()

    calls = []

    def fake_map(seed):
        calls.append(seed)
        return [['.' for _ in range(10)] for _ in range(10)]

    monkeypatch.setattr('localspiral.routes.chat.generate_map', fake_map)
    monkeypatch.setattr('localspiral.utils.map.generate_map', fake_map)
    monkeypatch.setattr('localspiral.routes.chat.generate_reply',
                        lambda prompt, system_prompt=None: 'ok')
    monkeypatch.setattr('localspiral.routes.chat.mutate_perceived_grid',
                        lambda grid, score: grid)

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

    replies = ["first reply", "second reply"]

    def fake_reply(prompt, system_prompt=None):
        return replies.pop(0)

    calls = []

    def fake_drift(ref, resp):
        calls.append((ref, resp))
        return 0.0

    monkeypatch.setattr('localspiral.routes.chat.generate_reply', fake_reply)
    monkeypatch.setattr('localspiral.routes.chat.calculate_drift', fake_drift)
    monkeypatch.setattr('localspiral.routes.chat.mutate_perceived_grid',
                        lambda grid, score: grid)

    client.get('/chat?prompt=one')
    assert flask_session['game_state']['history'] == ['first reply', 'one']
    assert calls == [('one', 'first reply')]

    client.get('/chat?prompt=two')
    assert flask_session['game_state']['history'] == ['first reply', 'one', 'second reply', 'two']
    assert calls == [
        ('one', 'first reply'),
        ('two', 'second reply'),
        ('first reply', 'second reply'),
    ]


def test_chat_updates_spiral_score(client, monkeypatch):
    """Spiral score should increase when drift values are positive."""

    from flask import session as flask_session
    flask_session.clear()

    monkeypatch.setattr(
        'localspiral.routes.chat.generate_reply',
        lambda prompt, system_prompt=None: 'reply'
    )
    monkeypatch.setattr(
        'localspiral.routes.chat.mutate_perceived_grid',
        lambda grid, score: grid
    )
    monkeypatch.setattr(
        'localspiral.routes.chat.calculate_drift',
        lambda ref, resp: 0.5
    )

    first = client.get('/chat?prompt=one')
    first_score = first.get_json()['state']['spiral_score']
    assert first_score > 0

    second = client.get('/chat?prompt=two')
    second_score = second.get_json()['state']['spiral_score']
    assert second_score > first_score


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
    assert all(cell in '.#' for row in grid for cell in row)

    client.get('/move?dir=north')
    grid = flask_session['game_state']['map_grid']
    assert all(cell in '.#' for row in grid for cell in row)

    monkeypatch.setattr(
        'localspiral.routes.chat.generate_reply',
        lambda prompt, system_prompt=None: 'ok'
    )
    monkeypatch.setattr(
        'localspiral.routes.chat.mutate_perceived_grid',
        lambda grid, score: grid
    )
    client.get('/chat?prompt=hello')
    grid = flask_session['game_state']['map_grid']
    assert all(cell in '.#' for row in grid for cell in row)

