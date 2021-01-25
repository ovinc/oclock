"""Test accuracy of timer for constant-duration loops."""

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
from random import random
from queue import Queue

import numpy as np

from . import Timer, measure_duration


def constant_duration_loop(timer, q, fracmax=0.5, n=10):
    """Try maintain loop timing constant with a function of random timing.

    - timer is a timer object from the oclock module
    - q is a queue that sends the data away from the loop for plotting
    - fracmax is the max fraction of the interval the random time can be
    - n is the number of loops
    """
    ts = []  # stores the times of the loop after the checkpt() call
    rs = []  # stores the random times generated

    timer.reset()  # Not obligatory, but ensures timing is counted from here.

    t0 = time.perf_counter()
    ts.append(t0)

    for i in range(n):

        # wait for a random time between 0 and the total requested interval / 2
        with measure_duration() as duration:
            r = timer.interval * fracmax * random()
            time.sleep(r)
        sleeptime = duration['duration (s)']

        # this is where the timer adapts the wait time to the execution time
        # of the lines above.
        timer.checkpt()

        t = time.perf_counter()

        ts.append(t)
        rs.append(sleeptime)

    return np.array(ts), np.array(rs)


def performance_test(dt, nloops, fmax, plot=False, warnings=False, precise=False):
    """Test accuracy of the constant-loop timing using random timing in loop.

    - dt is the requested total duration of the loop
    - nloops is the total number of loops
    - fmax is the max fraction of dt that can be taken by the random time.
    - plot: if True, show plot (matplotlib) of timing of all loops
    - warnings: if True, prints a warning when time interval too short
    - precise: if True, increase time precision (useful for Windows)
    """
    timer = Timer(interval=dt, warnings=warnings, precise=precise)
    q = Queue()

    print('Test Started')
    ts, rs = constant_duration_loop(timer, q, fmax, nloops)
    print('Test Finished')

    dts = np.diff(ts)
    avg = dts.mean()
    dev = dts.std()

    print("Mean dt (s): {}, std: {}".format(avg, dev))
    print("Mean dt - Requested dt (ms): {}".format((avg - dt) * 1000))
    print("Std dev (ms): {}".format(dev * 1000))

    if plot:

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 4))

        n = len(dts)
        ii = range(1, n + 1)

        ax.plot([1, n], [dt * 1000, dt * 1000], '-', c='antiquewhite',
                linewidth=6, label='requested duration')

        ax.fill_between(ii, rs * 1000, label='random time', color='0.9')

        ax.plot(ii, dts * 1000, '.', c='steelblue',
                label='individual loop duration')

        ax.plot([1, n], [avg * 1000, avg * 1000], ':', c='sandybrown',
                linewidth=4, label='average loop duration')

        ax.set_xlim((1, n))
        ax.set_ylim((0, dts.max() * 1050))

        ax.set_xlabel('loop number')
        ax.set_ylabel(r'$\Delta t$ (ms)')

        ax.grid()
        ax.legend()
        plt.show()

    return {'mean dt (s)': avg, 'std dev (s)': dev}
