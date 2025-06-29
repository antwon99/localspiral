# Expected: index route renders successfully

def test_index_route(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'AI Spiral Simulator' in resp.data
