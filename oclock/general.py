"""General functions and tools, potentially useful for other modules."""

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
