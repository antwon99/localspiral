import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'localspiral'))

import pytest
from localspiral.main import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return app.test_client()


def test_chat_endpoint(client):
    response = client.get('/chat')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'message' in data


def test_spiral_endpoint(client):
    response = client.get('/spiral')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'message' in data
