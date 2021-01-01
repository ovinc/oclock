"""Test accuracy of timer for constant-duration loops."""

import time
from random import random
from queue import Queue

import numpy as np

from . import Timer


def random_wait(tmax):
    """Waits for a random time between 0 and tmax."""
    t = tmax * random()
    time.sleep(t)
    return t


def constant_duration_loop(timer, q, fracmax=0.5, n=10):
    """Try maintain loop timing constant with a function of random timing.

    - timer is a timer object from the oclock module
    - q is a queue that sends the data away from the loop for plotting
    - fracmax is the max fraction of the interval the random time can be
    - n is the number of loops
    """
    timer.reset()  # Not obligatory, but ensures timing is counted from here.
    ts = []  # stores the times of the loop after the checkpt() call
    rs = []  # stores the random times generated

    for i in range(n):

        # wait for a random time between 0 and the total requested interval / 2
        r = random_wait(timer.interval * fracmax)

        # this is where the timer adapts the wait time to the execution time
        # of the lines above.
        timer.checkpt()

        t = time.time()

        ts.append(t)
        rs.append(r)

    return ts, rs


def performance_test(dt, nloops, fmax, plot=False):
    """Test accuracy of the constant-loop timing using random timing in loop.

    - dt is the requested total duration of the loop
    - nloops is the total number of loops
    - fmax is the max fraction of dt that can be taken by the random time.
    - plot: if True, show plot (matplotlib) of timing of all loops
    """
    timer = Timer(interval=dt)
    q = Queue()

    print('Test Started')
    ts, rs = constant_duration_loop(timer, q, fmax, nloops)
    print('Test Finished')

    dts = np.diff(ts)

    avg = dts.mean()
    dev = dts.std()

    print(f'Mean dt (s): {avg}, std: {dev}')
    print(f'Mean dt - Requested dt (ms): {(avg - dt) * 1000}')
    print(f'Percentage deviation: {100*(avg - dt)/dt:.4f}%')
    print(f'Std dev (ms): {dev * 1000}')

    if plot:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.plot(rs[1:], label='random time')
        ax.plot(dts, label='loop duration')
        ax.set_ylim((0, 1.5 * dt))
        ax.set_xlabel('loop number')
        ax.set_ylabel('dt (s)')
        ax.grid()
        ax.legend()
        plt.show()

    return {'mean dt (s)': avg, 'std dev (s)': dev}
