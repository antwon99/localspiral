import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.spiral import SpiralSystem


def test_apply_drift_increases_score():
    """Spiral score should accumulate with each drift application."""
    system = SpiralSystem()
    system.apply_drift(10)
    assert system.spiral_score == 10
    system.apply_drift(5)
    assert system.spiral_score == 15


def test_breaking_point_when_score_reaches_100():
    system = SpiralSystem()
    system.apply_drift(99)
    assert not system.breaking_point
    system.apply_drift(1)
    assert system.breaking_point
