"""Test accuracy of timer for constant-duration loops."""

import time

from queue import Queue

import matplotlib.pyplot as plt
import numpy as np

from . import Timer
from .example import random_wait


def constant_duration_loop(timer, q, fracmax=0.5, n=10):
    """Try maintain loop timing constant with a function of random timing.

    - timer is a timer object from the oclock module
    - q is a queue that sends the data away from the loop for plotting
    - fracmax is the max fraction of the interval the random time can be
    - n is the number of loops
    """

    timer.reset()  # Not obligatory, but ensures timing is counted from here.
    ts = []  # stores the times of the loop after the pause() call
    rs = []  # stores the random times generated

    for i in range(n):

        # wait for a random time between 0 and the total requested interval / 2
        r = random_wait(timer.interval * fracmax)

        # this is where the timer adapts the wait time to the execution time
        # of the lines above.
        timer.pause()

        t = time.time()

        ts.append(t)
        rs.append(r)

    return ts, rs


def test(dt, nloops, fmax):
    """Test accuracy of the constant-loop timing using random timing in loop.

    - dt is the requested total duration of the loop
    - nloops is the total number of loops
    - fmax is the max fraction of dt that can be taken by the random time.
    """


    timer = Timer(interval=dt)
    q = Queue()

    print('Test Started')
    ts, rs = constant_duration_loop(timer, q, fmax, nloops)
    print('Test Finished')

    dts = np.diff(ts)

    avg = dts.mean()
    dev = dts.std()

    print(f'Mean dt: {avg}, std: {dev}')
    print(f'Mean dt / Requested dt: {avg / dt}')
    print(f'Percentage deviation: {100*(avg - dt)/dt:.4f}%')
    print(f'Std dev / Requested dt: {dev / dt}')


    plt.plot(rs[1:], label='random time')
    plt.plot(dts, label='loop duration')
    plt.ylim((0, 1.5 * dt))
    plt.xlabel('loop number')
    plt.ylabel('dt (s)')
    plt.legend()
    plt.show()

