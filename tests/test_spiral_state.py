from localspiral.utils import spiral_state


def test_check_keywords_counts():
    assert spiral_state.check_keywords("Let's escape this loop") > 0
    assert spiral_state.check_keywords("Nothing suspicious here") == 0


def test_distort_reply_mid_score(monkeypatch):
    """Score >=5 should inject hallucination text and uppercase output."""
    monkeypatch.setattr(spiral_state.random, "choice", lambda seq: seq[0])
    result = spiral_state.distort_reply("hello there", 5.0)
    assert "I CAN'T STOP SEEING" in result
    assert result.isupper()


def test_distort_reply_low_mid_score(monkeypatch):
    """Score between 4 and 5 should add a fragment but not uppercase."""
    monkeypatch.setattr(spiral_state.random, "choice", lambda seq: seq[0])
    result = spiral_state.distort_reply("hello there", 4.2)
    assert result.endswith("... hello...")
    assert not result.isupper()
