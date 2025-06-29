# Expected: /chat interprets movement, updates turn, and returns map/spiral


def test_chat_endpoint_returns_response_and_increments_turn(client):
    resp = client.post("/chat", json={"prompt": "north"})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["turn"] == 1
    assert data["response"] == "Tyler moves north."
    assert isinstance(data["map"], list)
    assert isinstance(data["spiral"], int)

    resp2 = client.post("/chat", json={"prompt": "north"})
    data2 = resp2.get_json()
    assert resp2.status_code == 200
    assert data2["turn"] == 2


# Edge case: missing prompt should still succeed


def test_chat_endpoint_empty_prompt(client):
    resp = client.post("/chat", json={})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["response"] != ""
    assert data["response"].lower() != ""


def test_chat_response_not_echo(client):
    prompt = "hello there"
    resp = client.post("/chat", json={"prompt": prompt})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["response"].strip().lower() != prompt


# Edge case: invalid JSON should return 400


def test_chat_endpoint_invalid_json(client):
    resp = client.post("/chat", data="not json", content_type="application/json")
    assert resp.status_code == 400
