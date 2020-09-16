"""Timer for loops of fixed duration, avoiding drift."""

import time
from threading import Event


class Timer:

    def __init__(self, interval=1, name='Timer', warnings=False):

        self.interval = interval
        self.stop_event = Event()

        self.interval_exceeded = False
        self.warnings = warnings

        self.init_time = time.time()   # is never modified after init
        self.start_time = time.time()  # can be reset during timer operation

        # This effectively starts the timer when __init__ is called.
        self.target = self.start_time + interval

        # Used for distinguishing timers if necessary
        self.name = name

    def pause(self):
        """Waits adequate amount of time to keep the interval constant."""

        now = time.time()

        if now < self.target:
            # if time before the previous pause has not exceeded the
            # required interval, set target to another multiple of the interval
            self.interval_exceeded = False
            w = self.target - now
            self.target += self.interval
            self.stop_event.wait(w)

        else:
            # if already passed target, move on immediately and set target
            # at a time dt from current time to try again.
            if not self.interval_exceeded and self.warnings:
                # to print only the first time the problem happens
                print(f"\nWarning, time interval too short for {self.name}.")
            self.interval_exceeded = True
            self.target = now + self.interval

    def elapsed_time(self, since_reset=True):
        """Elapsed time (in s) since last reset (default), or init."""
        if since_reset:
            return time.time() - self.start_time
        else:
            return time.time() - self.init_time

    def change_interval(self, interval):
        """Modify existing interval to a new value, effective immediately."""
        self.deactivate()
        self.interval = interval
        self.target = self.start_time + self.interval
        self.stop_event.clear()

    def reset(self):
        """Reset timer so that it counts the time interval from now on."""
        self.deactivate()
        self.start_time = time.time()
        self.target = self.start_time + self.interval
        self.stop_event.clear()

    def deactivate(self):
        """Cancel the current waiting immediately."""
        self.stop_event.set()
