import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.scoring import calculate_drift


def test_calculate_drift_identical():
    assert calculate_drift('hello world', 'hello world') == 0


def test_calculate_drift_different():
    assert calculate_drift('a b c', 'a b c d') > 0
