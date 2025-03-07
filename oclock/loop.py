"""Use the timer class for timed loops without drift."""

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


from threading import Thread
from functools import wraps

from . import Timer


# ============== Command Line Interface to interact with Timer ===============


def cli(timer):
    """Command line input to interact with a timer object.

    Possible Inputs
    ---------------
    - any number (int/float): change timer interval to that new value
    - 'p' or 'pause': pause timer
    - 'r' or 'resume': resume timer
    - 'R' or 'reset': reset timer
    - 't' or 'time': print timing (interval, elapsed time, etc.) info
    - 'q', 'Q', 'quit' or 'stop': stop timer and exit
    """
    msg = '-----------------------------------------------------------------\n'\
          'Timer Command-Line-Interface. Possible inputs:\n' \
          '- any number (int/float): change timer interval to that new value\n' \
          "- 'p' or 'pause': pause timer\n" \
          "- 'r' or 'resume': resume timer\n" \
          "- 'R' or 'reset': reset timer\n" \
          "- 't' or 'time': print timing (interval, elapsed time, etc.) info\n"\
          "- 'q', 'Q', 'quit' or 'stop': stop timer and exit\n" \
          '-----------------------------------------------------------------\n'
    print(msg)

    while not timer.is_stopped:
        a = input()
        try:
            dt = float(a)
        except ValueError:
            if a in ('p', 'pause'):
                print('--- Timer Paused')
                timer.pause()
            elif a in ('r', 'resume'):
                print('--- Timer Resumed')
                timer.resume()
            elif a in ('R', 'reset'):
                print('--- Timer Restarted')
                timer.reset()
            elif a in ('t', 'time'):
                elapsed = timer.elapsed_time
                paused = timer.pause_time
                dt = timer.interval
                tnext = timer.next_checkpt_release - timer.now()
                print("[Interval {:.3f}] [Elapsed: {:.3f}] [Paused {:.3f}] "
                      "[Next {:.3f}]".format(dt, elapsed, paused, tnext))
            elif a in ('q', 'Q', 'quit', 'stop'):
                print('--- Timer Stopped')
                timer.stop()
            else:
                pass
        else:
            try:
                timer.interval = dt
            except ValueError:
                print('--- Invalid Interval')
            else:
                print('--- Interval (s) changed to {}'.format(dt))

    print('--- Loop Exited')


# ========== Decorators to repeat function periodically using Timer ==========


def loop(timer):
    """Decorator to start a timed loop repeating a function periodically.

    Parameters
    ----------
    timer : oclock.Timer object
    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            while not timer.is_stopped:
                timer.checkpt()
                function(*args, **kwargs)
        return wrapper
    return decorator


def interactiveloop(**timer_kwargs):
    """Decorator to start an interactive CLI for timed execution of a function

    Parameters
    ----------
    any argument or keyword-argument taken by oclock.Timer(), e.g. 'interval'
    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            timer = Timer(**timer_kwargs)
            Thread(target=cli, args=(timer,)).start()
            timer.reset()  # removes any delay introduced by thread starting
            while not timer.is_stopped:
                function(*args, **kwargs)
                timer.checkpt()
        return wrapper
    return decorator
