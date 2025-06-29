from localspiral.main import app


def test_routes_exist():
    client = app.test_client()
    assert client.get('/').status_code == 200
    assert client.get('/map').status_code == 200
    assert client.get('/spiral').status_code == 200
    assert client.post('/chat', json={'prompt': 'hello'}).status_code == 200
    assert client.post('/reset').status_code == 200
