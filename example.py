"""Example of use of the timer class in an asynchronous environment."""


import time
from threading import Thread
from random import random

from oclock import Timer
from oclock.loop import cli


def timed_loop(timer):
    """Loop with function to be repeated at regular time intervals."""

    timer.reset()  # Not obligatory, but ensures timing is counted from here.

    while not timer.is_stopped:

        # Only to show timer status, for information
        print('elapsed time: {:.3f}, next checkpt at: {:.3f}'
              .format(timer.elapsed_time, timer.next_checkpt_release - timer.start_time))

        # wait for a random time between 0 and 100ms
        # (in real use, this would be the function to repeated in a timed manner)
        time.sleep(0.1 * random())

        # this is where the timer adapts the wait time to the execution time
        # of the lines above.
        timer.checkpt()


def main():
    """Run main_loop at the same time as the command line."""

    timer = Timer(interval=1.5, warnings=True)

    Thread(target=timed_loop, args=(timer,)).start()

    # CLI is a simple command line interface to interact with the timer
    cli(timer)

    print('Program Exited')


if __name__ == '__main__':
    main()
