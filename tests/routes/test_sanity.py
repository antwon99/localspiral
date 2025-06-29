def test_sanity_endpoint_returns_value(client):
    resp = client.get('/sanity')
    data = resp.get_json()
    assert resp.status_code == 200
    assert 'sanity' in data
