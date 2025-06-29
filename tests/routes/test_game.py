# Expected: /map returns map grid and /reset resets state

def test_map_endpoint_returns_map(client):
    resp = client.get('/map')
    data = resp.get_json()
    assert resp.status_code == 200
    assert isinstance(data['map'], list)
    assert len(data['map']) > 0


def test_reset_endpoint_resets_state(client):
    client.post('/chat', json={'prompt': 'hi'})
    resp = client.post('/reset')
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['status'] == 'reset'
