import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from localspiral.utils import scoring
from localspiral.utils.scoring import calculate_drift

import pytest


def test_calculate_drift_identical():
    assert calculate_drift('hello world', 'hello world') == pytest.approx(0.0, abs=1e-6)


def test_calculate_drift_different():
    score = calculate_drift('a b c', 'a b c d')
    assert 0 < score < 1
    assert score == pytest.approx(0.134, abs=1e-3)


def test_calculate_drift_openai(monkeypatch):
    def fake_embed(text):
        return [1.0, 0.0] if "hello" in text else [0.0, 1.0]

    monkeypatch.setattr(scoring, "_openai_embed", fake_embed)
    score = calculate_drift("hello", "world", use_openai=True)
    assert score == pytest.approx(1.0)
