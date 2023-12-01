"""General functions and tools for the oclock package."""

# ----------------------------- License information --------------------------

# This file is part of the oclock python package.
# Copyright (C) 2021 Olivier Vincent

# The oclock package is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# The oclock package is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with the oclock python package.
# If not, see <https://www.gnu.org/licenses/>


import time
from datetime import timedelta
from contextlib import contextmanager
from threading import Thread


def parse_time(time_str):
    """Transforms inputs in the form h:m:s into a timedelta.

    Input
    -----
    time_str: str (e.g. ::5 for 5 seconds or 1:30: for 1.5 hours)
    (see examples below)

    Output
    ------
    datetime.timedelta object

    Examples
    --------
    '3:14:16'   --> 3 hours, 14 minutes, 16 seconds
    '1:45:00'   --> 1 hour 45 minutes
    '1:45:'     --> 1 hour 45 minutes
    '00:02:00'  --> 2 minutes
    ':2:'       --> 2 minutes
    '00:00:05'  --> 5 seconds
    '::5'       --> 5 seconds
    """
    timestr = time_str.split(':')
    tint = []

    for tstr in timestr:
        try:
            t = int(tstr)
        except ValueError:
            t = 0
        tint.append(t)

    h, m, s = tint
    duration = timedelta(hours=h, minutes=m, seconds=s)
    return duration


@contextmanager
def measure_time():
    """Measure mean unix time (s) and time uncertainty (s) of encapsulated commands.

    Output
    ------
    Dictionary with keys:
        - 'time (unix)': (tmax + tmin) / 2
        - 'dt (s)': (tmax - tmin) / 2

    where tmin, tmax are the unix times before the instructions and after the
    instructions, respectively.

    Examples
    --------
    >>> with measure_time() as timing:
            my_function()
        print(timing)

    Out:
    {'time (unix)': 1604780958.0705943, 'dt (s)': 0.6218999624252319}

    >>> with measure_time() as data:
            measurement = my_function()  # returns e.g. 3.618
            data['measurement'] = measurement
        print(data)

    Out:
    {'measurement': 3.618,
     'time (unix)': 1604780958.0705943,
     'dt (s)': 0.6218999624252319}
    """
    timing = {}
    t1 = time.time()
    t1p = time.perf_counter()
    try:
        yield timing
    finally:
        t2 = time.time()
        t2p = time.perf_counter()
        dt = (t2p - t1p) / 2
        t = (t1 + t2) / 2
        timing['time (unix)'] = t
        timing['dt (s)'] = dt


@contextmanager
def measure_duration():
    """Measure duration (s) of encapsulated commands.

    Output
    ------
    Dict with total duration in seconds (key 'duration (s)')

    Example
    -------
    >>> with measure_duration() as duration:
            my_function()
        print(duration)

    Out:
    {'duration (s)': 0.9871297000004233}
    """
    duration = {}
    t1 = time.perf_counter()
    try:
        yield duration
    finally:
        t2 = time.perf_counter()
        duration['duration (s)'] = t2 - t1


def after(duration=':::', function=None, args=None, kwargs=None, blocking=True):
    """Execute function after given waiting time

    Input
    -----
    - duration: time to wait in a format h:m:s (see oclock.parse_time())
    - function: function to execute
    - args: arguments to pass to the function (tuple)
    - kwargs: keyword arguments to pass to the function (dict)
    - blocking: if True (default), blocks console until function executed.

    Output
    ------
    - if blocking: returns result of function
    - if non-blocking: returns None
    """
    wait_time = parse_time(duration).total_seconds()
    args = () if args is None else args
    kwargs = {} if kwargs is None else kwargs

    def exec_func():
        time.sleep(wait_time)
        return function(*args, **kwargs)

    if blocking:
        return exec_func()
    else:
        Thread(target=exec_func).start()
