"""Timer for loops of fixed duration, avoiding drift."""

import time
from threading import Event


class Timer:

    def __init__(self, interval=1):

        self.interval = interval
        self.stop_event = Event()
        self.interval_exceeded = False

        # This effectively starts the timer when __init__ is called.
        self.target = time.time() + interval

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
            if self.interval_exceeded:
                print("Warning, time interval too short.")
            self.interval_exceeded = True
            self.target = now + self.interval

    def change_interval(self, interval):
        """Modify the existing interval to a new value."""
        self.deactivate()
        self.interval = interval
        self.reset()

    def reset(self):
        """Reset timer so that it counts the time interval"""
        self.deactivate()
        self.target = time.time() + self.interval
        self.stop_event.clear()

    def deactivate(self):
        """Cancel the current waiting immediately."""
        self.stop_event.set()
