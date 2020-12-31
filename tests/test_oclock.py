"""Test oclock module with pytest"""


import time

from oclock.performance import performance_test
from oclock import parse_time, measure_time, countdown


def test_timer():
    """Test Timer() class."""
    data = performance_test(dt=0.05, nloops=40, fmax=0.9, plot=False)
    assert round(data['mean dt (s)'], 2) == 0.05


def test_parse():
    """Test parsing of time strings."""
    t1 = parse_time('::5')
    t2 = parse_time('1::')
    t3 = parse_time('2:30:25')
    t4 = parse_time('::')

    ts = t1, t2, t3, t4
    ss = 5, 3600, 9025, 0

    for t, s in zip(ts, ss):
        assert t.total_seconds() == s


def test_measure():
    """Test measure_time() context manager."""
    with measure_time() as timing:
        time.sleep(1)
    assert round(timing['dt (s)'], 1) == 0.5


def test_countdown():
    """Test interactive countdown."""
    countdown('::5')
