"""Example of use of the timer class in an asynchronous environment."""

import time
from threading import Event
from concurrent import futures
from random import random

from oclock import Timer


def random_wait(tmax):
    """Waits for a random time between 0 and tmax."""
    t = tmax * random()
    time.sleep(t)
    return t


def command_line(e_exit, timer):
    """Input value of dt in s, or any non-number to exit."""

    while not e_exit.is_set():

        a = input()

        try:
            dt = float(a)
        except ValueError:
            e_exit.set()
            timer.deactivate()
        else:
            timer.change_interval(dt)


def main_loop(e_exit, timer):
    """Prints time since start, with pause at checkpoint managed by timer."""

    t0 = time.time()
    timer.reset()  # Not obligatory, but ensures timing is counted from here.

    while not e_exit.is_set():

        # wait for a random time between 0 and the total requested interval
        random_wait(timer.interval)

        # this is where the timer adapts the wait time to the execution time
        # of the lines above.
        timer.pause()

        # The lines below are just for visual testing during execution
        t = time.time()
        dt = t - t0
        print(f'current time: {dt:.3f}, next target: {timer.target - t0:.3f}')


def main():
    """Run main_loop at the same time as the command line."""

    timer = Timer(interval=2)
    e_exit = Event()

    with futures.ThreadPoolExecutor() as executor:
        executor.submit(command_line, e_exit, timer)
        print('Type new interval in s or any other input to exit')
        main_loop(e_exit, timer)


if __name__ == '__main__':
    main()
