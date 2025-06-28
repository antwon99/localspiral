import pytest
from localspiral.main import create_app
from localspiral.utils import dialogue


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
    response = client.get('/chat?prompt=hello')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'ok'
    assert 'state' in data
    assert 'spiral_score' in data['state']


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
    assert 'seed' in first.get_json()


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

    first = client.get('/chat?prompt=one')
    assert first.status_code == 200
    assert len(calls) == 1

    second = client.get('/chat?prompt=two')
    assert second.status_code == 200
    assert len(calls) == 1
