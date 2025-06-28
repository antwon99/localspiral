import pytest
from localspiral.config import get_openai_api_key


def test_get_openai_api_key(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'sk-test')
    assert get_openai_api_key() == 'sk-test'


def test_get_openai_api_key_missing(monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    with pytest.raises(RuntimeError):
        get_openai_api_key()
