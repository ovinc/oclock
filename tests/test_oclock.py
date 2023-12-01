"""Test oclock module with pytest"""

import time
import threading
import random

from oclock.performance import performance_test
from oclock import Timer, Countdown, loop
from oclock import parse_time, measure_time, measure_duration, after


def test_timer():
    """Test Timer() class (checkpt() and interval)"""
    data = performance_test(dt=0.05, nloops=40, fmax=0.9, plot=False)
    assert round(data['mean dt (s)'], 2) == 0.05


def test_timer_precise():
    """Test Timer() class in precise mode (precision not tested here)"""
    data = performance_test(dt=0.05, nloops=40, fmax=0.9, plot=False, precise=True)
    assert round(data['mean dt (s)'], 2) == 0.05


def test_decorator():
    """Test the @loop decorator and various Timer methods"""

    timer = Timer(interval=0.1)
    dt = 0.6  # interval between commands

    def timer_control(timer):
        """define a succession of commands to apply to the timer."""
        methods = timer.reset, timer.pause, timer.resume, timer.stop
        print('timer interval: {}'.format(timer.interval))
        print('interval between commands: {}'.format(dt))
        for method in methods:
            time.sleep(dt)
            print(method)
            print('elapsed/paused before method: {:.3f}/{:.3f}'
                  .format(timer.elapsed_time, timer.pause_time))
            method()
            print('elapsed/paused after method: {:.3f}/{:.3f}'
                  .format(timer.elapsed_time, timer.pause_time))

    @loop(timer)
    def my_function():
        time.sleep(0.05 * random.random())

    threading.Thread(target=timer_control, args=(timer,)).start()
    my_function()

    assert round(timer.elapsed_time, 1) == 2 * dt
    assert round(timer.pause_time, 1) == dt


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


def test_measure_time():
    """Test measure_time() context manager."""
    with measure_time() as timing:
        time.sleep(1)
    assert round(timing['dt (s)'], 1) == 0.5


def test_measure_duration():
    """Test measure_time() context manager."""
    with measure_duration() as duration:
        time.sleep(1)
    assert round(duration['duration (s)'], 1) == 1


def test_after():
    """Test after() function"""
    def my_function():
        print('Hello')
        return 3.14
    result = after('::1', my_function)
    assert result == 3.14


def test_countdown():
    """Test interactive countdown."""
    countdown = Countdown('::5')
    assert countdown.done
