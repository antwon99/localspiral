from localspiral.utils import scoring
from localspiral.utils.scoring import calculate_drift

import pytest


def test_calculate_drift_identical(monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    assert calculate_drift('hello world', 'hello world') == pytest.approx(0.0, abs=1e-6)


def test_calculate_drift_different(monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    score = calculate_drift('a b c', 'a b c d')
    assert 0 < score < 1
    assert score == pytest.approx(0.134, abs=1e-3)


def test_calculate_drift_openai(monkeypatch):
    calls = []

    def fake_embed(text: str, model: str = 'text-embedding-3-small'):
        calls.append(text)
        return [1.0, 0.0] if text == 'x' else [0.0, 1.0]

    monkeypatch.setenv('OPENAI_API_KEY', 'sk-test')
    monkeypatch.setattr(scoring, '_openai_embed', fake_embed)

    score = calculate_drift('x', 'y')
    assert calls == ['x', 'y']
    assert score == pytest.approx(1.0, abs=1e-6)
