"""Test accuracy of timer for constant-duration loops."""

import time
from random import random
from queue import Queue

import numpy as np

from . import Timer


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
        r = timer.interval * fracmax * random()
        time.sleep(r)

        # this is where the timer adapts the wait time to the execution time
        # of the lines above.
        timer.checkpt()

        t = time.perf_counter()

        ts.append(t)
        rs.append(r)

    return ts, rs


def performance_test(dt, nloops, fmax, plot=False, warnings=False):
    """Test accuracy of the constant-loop timing using random timing in loop.

    - dt is the requested total duration of the loop
    - nloops is the total number of loops
    - fmax is the max fraction of dt that can be taken by the random time.
    - plot: if True, show plot (matplotlib) of timing of all loops
    - warnings: if True, prints a warning when time interval too short
    """
    timer = Timer(interval=dt, warnings=warnings)
    q = Queue()

    print('Test Started')
    ts, rs = constant_duration_loop(timer, q, fmax, nloops)
    print('Test Finished')

    dts = np.diff(ts)
    avg = dts.mean()
    dev = dts.std()

    print(f'Mean dt (s): {avg}, std: {dev}')
    print(f'Mean dt - Requested dt (ms): {(avg - dt) * 1000}')
    print(f'Std dev (ms): {dev * 1000}')

    if plot:

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()

        n = len(dts)
        ii = range(1, n + 1)

        ax.fill_between(ii, rs, label='random time', color='0.9')
        ax.plot([1, n], [dt, dt], '-', c='0.7', linewidth=3, label='requested')
        ax.plot([1, n], [avg, avg], '--', c='0.4', linewidth=2, label='average')
        ax.plot(ii, dts, '.k', label='loop duration')

        ax.set_xlim((1, n))
        ax.set_ylim((0, dts.max() * 1.05))

        ax.set_xlabel('loop number')
        ax.set_ylabel('dt (s)')

        ax.grid()
        ax.legend()
        plt.show()

    return {'mean dt (s)': avg, 'std dev (s)': dev}
