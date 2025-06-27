from localspiral.utils.scoring import calculate_drift

import pytest


def test_calculate_drift_identical():
    assert calculate_drift('hello world', 'hello world') == pytest.approx(0.0, abs=1e-6)


def test_calculate_drift_different():
    score = calculate_drift('a b c', 'a b c d')
    assert 0 < score < 1
    assert score == pytest.approx(0.134, abs=1e-3)
