import os
import sys
import json

stubs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'stubs'))
sys.path.insert(0, stubs_path)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'localspiral'))

import pytest

from localspiral.utils import dialogue


class DummyResponse:
    def __init__(self, body: str):
        self._body = body

    def read(self):
        return self._body.encode('utf-8')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_generate_reply(monkeypatch):
    payload = {"choices": [{"message": {"content": "hi"}}]}

    def fake_urlopen(req):
        body = json.dumps(payload)
        return DummyResponse(body)

    monkeypatch.setenv('OPENAI_API_KEY', 'sk-test')
    monkeypatch.setattr(dialogue, 'request', dialogue.request)
    monkeypatch.setattr(dialogue.request, 'urlopen', fake_urlopen)
    result = dialogue.generate_reply('hello')
    assert result == 'hi'
