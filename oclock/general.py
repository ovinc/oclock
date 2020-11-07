"""General functions and tools, potentially useful for other modules."""


import time
from contextlib import contextmanager


def parse_time(time_string):
    """Transforms inputs in the form h:m:s in a h, m, s tuple.

    Examples
    --------
    '3:14:16'   --> 3, 14, 16    (3 hours, 14 minutes, 16 seconds)
    '1:45:00'   --> 1, 45, 0     (1 hour 45 minutes)
    '1:45:'     --> 1, 45, 0     (1 hour 45 minutes)
    '00:02:00'  --> 0, 2, 0      (2 minutes)
    ':2:'       --> 0, 2, 0      (2 minutes)
    '00:00:05'  --> 0, 0, 5      (5 seconds)
    '::5'       --> 0, 0, 5      (5 seconds)
    """
    timestr = time_string.split(':')
    tint = []

    for tstr in timestr:
        try:
            t = int(tstr)
        except ValueError:
            t = 0
        tint.append(t)

    return tuple(tint)


@contextmanager
def measure_time():
    """Measure mean unix time (s) and time uncertainty (s) of encapsulated commands.

    Returns a dict with keys:
        - 'time (unix)': (tmax + tmin) / 2
        - 'dt (s)': (tmax - tmin) / 2

    where tmin, tmax are the unix times before the instructions and after the
    instructions, respectively.

    Example of use as a context manager:
    >>> with measure_time() as timing:
            my_function()
        print(timing)
    {'time (unix)': 1604780958.0705943, 'dt (s)': 0.6218999624252319}
    """
    timing = {}
    t1 = time.time()
    try:
        yield timing
    finally:
        t2 = time.time()
        dt = (t2 - t1) / 2
        t = t1 + dt / 2
        timing['time (unix)'] = t
        timing['dt (s)'] = dt


@contextmanager
def measure_time():
    """Measure mean unix time (s) and time uncertainty (s) of encapsulated commands.

    Returns a dict with keys:
        - 'time (unix)': (tmax + tmin) / 2
        - 'dt (s)': (tmax - tmin) / 2

    where tmin, tmax are the unix times before the instructions and after the
    instructions, respectively.

    Example of uses as a context manager:
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
    try:
        yield timing
    finally:
        t2 = time.time()
        dt = (t2 - t1) / 2
        t = t1 + dt / 2
        timing['time (unix)'] = t
        timing['dt (s)'] = dt
