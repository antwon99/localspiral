import os
import sys

stubs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'stubs'))
sys.path.insert(0, stubs_path)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'localspiral'))

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
    monkeypatch.setattr('localspiral.routes.chat.generate_reply', lambda prompt: 'ok')
    response = client.get('/chat?prompt=hello')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'ok'


def test_spiral_endpoint(client):
    response = client.get('/spiral')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'message' in data


def test_map_endpoint(client):
    first = client.get('/map?seed=5')
    second = client.get('/map?seed=5')
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.get_json()['grid'] == second.get_json()['grid']
