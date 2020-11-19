"""Timer for loops of fixed duration, avoiding drift."""

import time
from threading import Event


class Timer:

    def __init__(self, interval=1, name='Timer', warnings=False):

        self._interval = interval
        self.stop_event = Event()

        self.interval_exceeded = False
        self.paused = False
        self.warnings = warnings

        self.init_time = time.time()   # is never modified after init
        self.start_time = time.time()  # can be reset during timer operation
        self._pause_time = 0       # amount of time the system has been paused

        # This effectively starts the timer when __init__ is called.
        self.target = self.start_time + interval

        # Used for distinguishing timers if necessary
        self.name = name

    def __repr__(self):
        warning = 'on' if self.warnings else 'off'
        s = f"{self.__class__}, name '{self.name}', interval {self.interval}s, " \
            f'warnings {warning.upper()}'
        return s

    def checkpt(self):
        """Waits at current point in program to keep the interval constant."""

        now = time.time()

        if now < self.target:
            # if time before the previous checkpt has not exceeded the
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

    @property
    def pause_time(self):
        if self.paused:
            now = time.time()
            return self._pause_time + now - self.pause_t1
        else:
            return self._pause_time

    @property
    def elapsed_time(self):
        """Elapsed time (in s) since last reset or init (if no reset)."""
        now = time.time()
        return now - self.start_time - self.pause_time

    def reset(self):
        """Reset timer so that it counts the time from now on."""
        now = time.time()
        self.deactivate()
        self._pause_time = 0
        self.start_time = now
        self.target = now + self.interval
        self.stop_event.clear()

    def deactivate(self):
        """Cancel the current waiting immediately."""
        self.stop_event.set()

    def pause(self):
        """Pause timer until it is restarted."""
        if not self.paused:   # do nothing if timer is already paused
            self.pause_t1 = time.time()
            self.paused = True

    def resume(self):
        """Restart timer after pause event."""
        if self.paused:   # do nothing if timer is not paused
            self.pause_t2 = time.time()
            self._pause_time += self.pause_t2 - self.pause_t1
            self.paused = False
            self.pause_t1, self.pause_t2 = None, None  # reset pause time measurement

    @property
    def interval(self):
        """Interval property: time interval of the Timer object."""
        return self._interval

    @interval.setter
    def interval(self, value):
        """Modify existing interval to a new value, effective immediately."""
        now = time.time()
        self.deactivate()
        self._interval = value
        self.target = now + value
        self.stop_event.clear()
