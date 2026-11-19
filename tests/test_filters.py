import pytest
from pc_monitor.filters import ExponentialMovingAverage, moving_average


def test_sma():
    assert moving_average([10, 20, 30, 40, 50]) == 30


def test_sma_spike_is_damped():
    # одиночный выброс 100 % на фоне 10 % после сглаживания по 5 даёт всего 28 %
    assert moving_average([10, 10, 100, 10, 10]) == 28


def test_sma_empty():
    with pytest.raises(ValueError):
        moving_average([])


def test_ema():
    e = ExponentialMovingAverage(5)          # alpha = 1/3
    assert e.update(30) == 30
    assert e.update(60) == pytest.approx(40)
