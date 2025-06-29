# Expected: /chat returns placeholder response and increments turn

def test_chat_endpoint_returns_response_and_increments_turn(client):
    resp = client.post('/chat', json={'prompt': 'hello'})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['turn'] == 1
    assert data['response'] == 'Tyler hears: hello'

# Edge case: missing prompt should still succeed

def test_chat_endpoint_empty_prompt(client):
    resp = client.post('/chat', json={})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['response'] == 'Tyler hears: '

# Edge case: invalid JSON should return 400

def test_chat_endpoint_invalid_json(client):
    resp = client.post('/chat', data='not json', content_type='application/json')
    assert resp.status_code == 400
