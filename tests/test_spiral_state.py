import pytest
from localspiral.utils.spiral_state import check_keywords


def test_check_keywords_counts():
    assert check_keywords("Let's escape this loop") > 0
    assert check_keywords("Nothing suspicious here") == 0
