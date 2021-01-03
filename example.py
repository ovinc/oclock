"""Example of use of the timer class in an asynchronous environment."""


import time
from threading import Thread
from random import random

from oclock import Timer


def user_input(timer):
    """Command line input to change the time interval of the timer or exit.

    To change time interval: input value of time interval (s)
    To exit: input any non-number to exit.
    """
    while not timer.is_stopped:
        a = input()
        try:
            dt = float(a)
        except ValueError:
            timer.stop()
        else:
            timer.interval = dt


def timed_loop(timer):
    """Loop with function to be repeated at regular time intervals."""

    timer.reset()  # Not obligatory, but ensures timing is counted from here.

    while not timer.is_stopped:

        # Only to show timer status, for information
        print('elapsed time: {:.3f}, next target: {:.3f}'
              .format(timer.elapsed_time, timer.target - timer.start_time))

        # wait for a random time between 0 and 100ms
        # (in real use, this would be the function to repeated in a timed manner)
        time.sleep(0.1 * random())

        # this is where the timer adapts the wait time to the execution time
        # of the lines above.
        timer.checkpt()


def main():
    """Run main_loop at the same time as the command line."""

    timer = Timer(interval=1.5, warnings=True)

    thread1 = Thread(target=timed_loop, args=(timer,))
    thread2 = Thread(target=user_input, args=(timer,))
    threads = thread1, thread2

    print('Input value of time interval (s) or any non-number to exit')

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print('Program Exited')


if __name__ == '__main__':
    main()
