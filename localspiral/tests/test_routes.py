from localspiral.main import app


def test_routes_exist():
    client = app.test_client()
    resp = client.get('/map')
    assert resp.status_code == 200
    resp = client.get('/spiral')
    assert resp.status_code == 200
    resp = client.post('/chat', json={'prompt': 'hello'})
    assert resp.status_code == 200
    resp = client.post('/reset')
    assert resp.status_code == 200
