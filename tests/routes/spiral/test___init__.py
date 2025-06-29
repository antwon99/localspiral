# Expected: /spiral returns current spiral score

def test_spiral_endpoint_returns_score(client):
    resp = client.get('/spiral')
    data = resp.get_json()
    assert resp.status_code == 200
    assert 'spiral' in data
