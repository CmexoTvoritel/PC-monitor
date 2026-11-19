import pytest
from pc_monitor.ring_buffer import RingBuffer


def test_fill_and_last():
    b = RingBuffer(5)
    for v in [1, 2, 3]:
        b.append(v)
    assert len(b) == 3
    assert b.last(2) == [2, 3]
    assert b.last(10) == [1, 2, 3]


def test_overwrite_oldest():
    b = RingBuffer(3)
    for v in range(1, 6):          # 1..5 в буфер на 3
        b.append(v)
    assert len(b) == 3
    assert b.items() == [3, 4, 5]


def test_capacity_600_is_ten_minutes():
    b = RingBuffer(600)
    for v in range(1000):
        b.append(v)
    assert len(b) == 600 and b.items()[0] == 400


def test_bad_capacity():
    with pytest.raises(ValueError):
        RingBuffer(0)
