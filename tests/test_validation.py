import math
from pc_monitor.validation import is_valid


def test_valid_range():
    assert is_valid(0) and is_valid(55.5) and is_valid(100)


def test_invalid():
    for v in [-1, 100.1, math.nan, math.inf, None, "50", True]:
        assert not is_valid(v)
