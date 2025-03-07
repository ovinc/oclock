"""Timer for loops of fixed duration, avoiding drift."""

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


import time
import threading
from .event import Event


class Timer:
    """Timer that is cancellable and modifiable in real time."""

    def __init__(self, interval=1, name='Timer', warnings=False, precise=False):
        """Init oclock.Timer object.

        Parameters
        ----------
        interval : int or float
            timer interval in seconds
            (default 1)

        name : str
            optional name for description purposes (repr and warnings)
            (default 'Timer')

        warnings : bool
            If True, prints warning when time interval exceeded
            (default False)

        precise : bool
            if True, increase time precision ; useful for Windows
            (default False)
        """
        self._interval = interval
        self._interval_failed = False

        self.warnings = warnings
        self.name = name

        # used to bypass waiting time when changes or stopping are required
        self._bypass_checkpt = Event() if precise else threading.Event()
        # used to wait for timer reactivation when in a paused state
        self._unpause_event = Event() if precise else threading.Event()

        self._start()      # Timer starts automatically upon init

    def __repr__(self):
        """Str representation of Timer object"""
        warning = 'ON' if self.warnings else 'OFF'
        s = "{}, name '{}', interval {}s, warnings {}" \
            .format(self.__class__, self.name, self.interval, warning)
        return s

    def _start(self):
        """Start timer (not for public use)."""
        now = self.now()
        self.start_time = now
        self._target = now + self._interval
        self.next_checkpt_release = self._target
        self._pause_time = 0
        self._bypass_checkpt.clear()
        self.is_paused = False
        self.is_stopped = False

    def reset(self):
        """Reset timer immediately."""
        if self.is_paused:
            self.resume()
        self._bypass_checkpt.set()
        self._start()

    def stop(self):
        """Stop timer immediately."""
        if self.is_paused:
            self.resume()
        self._unpause_event.set()      # in case stop is called in a paused state
        self._bypass_checkpt.set()  # cancel any remaining wait at the checkpt
        self.stop_time = self.now()
        self.is_stopped = True

    def pause(self):
        """Pause timer immediately, until it is resumed with resume()."""
        # do nothing if timer is already paused (also inactive if timer stopped)
        if not self.is_paused and not self.is_stopped:
            self._bypass_checkpt.set()
            self._unpause_event.clear()
            self._pause_init_time = self.now()
            self.is_paused = True

    def resume(self):
        """Resume timer after pause event."""
        # do nothing if timer is not paused (also inactive if timer stopped)
        if self.is_paused and not self.is_stopped:
            self._pause_time += self.now() - self._pause_init_time
            self.is_paused = False
            self._unpause_event.set()

    def checkpt(self):
        """Waits at current point in program to keep the interval constant."""

        if self.is_paused:  # if timer is paused, wait for reactivation by resume()

            self._unpause_event.wait()

            # The two lines below (target adjustment and else statement) make
            # the program liberate the checkpt immediately after a pause, and
            # sets the next checkpt one interval away
            self._target = self.now() + self._interval

        else:

            if not self.interval_exceeded:

                # if time before the previous checkpt has not exceeded the
                # required interval, set target to another multiple of dt

                if self.warnings and self._interval_failed:
                    # only called when interval is ok again after having failed
                    print("--- Time interval ({}s) OK again for {}"
                          .format(self.interval, self.name))
                self._interval_failed = False

                w = self._target - self.now()
                self._target += self._interval
                self._bypass_checkpt.wait(w)

            else:

                # if already passed target, move on immediately and set target
                # at a time dt from current time to try again.

                if self.warnings and not self._interval_failed:
                    # only called when interval fails right after being ok
                    print("--- Warning, time interval ({}s) too short for {}"
                          .format(self.interval, self.name))
                self._interval_failed = True

                self._target = self.now() + self.interval

        # always reset the bypass event after a checkpt
        self._bypass_checkpt.clear()
        self.next_checkpt_release = self._target

    @property
    def pause_time(self):
        """Total duration (s) during which the timer has been paused."""
        if self.is_paused and not self.is_stopped:
            now = self.now()
            return self._pause_time + now - self._pause_init_time
        else:
            return self._pause_time

    @property
    def total_time(self):
        """Total time (s) since init or reset, stops with timer.stop()."""
        t = self.now() if not self.is_stopped else self.stop_time
        return t - self.start_time

    @property
    def elapsed_time(self):
        """Elapsed time (in s) since init or reset."""
        return self.total_time - self.pause_time

    @property
    def interval(self):
        """Interval property: time interval of the Timer object."""
        return self._interval

    @interval.setter
    def interval(self, value):
        """Modify existing interval to a new value, effective immediately."""
        self.set_interval(value, immediate=True)

    def set_interval(self, value, immediate=True):
        """Choose if interval change is effective immediately or at next checkpt"""
        if value < 0:
            raise ValueError('Timer interval must be positive')
        self._interval = value
        if immediate:
            self._target = self.now() + value
            self._bypass_checkpt.set()

    @property
    def interval_exceeded(self):
        if self.now() < self._target:
            return False
        else:
            return True

    @staticmethod
    def now():
        """Define what is considered as current time"""
        return time.perf_counter()
