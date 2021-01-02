"""Timer for loops of fixed duration, avoiding drift."""


import time
from threading import Event


class Timer:
    """Timer that is cancellable and modifiable in real time."""

    def __init__(self, interval=1, name='Timer', warnings=False):
        """Init oclock.Timer object.

        Parameters
        ----------
        interval (float): timer interval in seconds
        name (str): optional name for description purposes (repr and warnings)
        warnings (bool): If True, prints warning when time interval exceeded
        """
        self._interval = interval
        self._interval_failed = False

        self.warnings = warnings
        self.name = name

        # used to bypass waiting time when changes or stopping are required
        self._bypass_checkpt = Event()
        # used to wait for timer reactivation when in a paused state
        self._unpause_event = Event()

        self._start()      # Timer starts automatically upon init

    def __repr__(self):
        """Str representation of Timer object"""
        warning = 'ON' if self.warnings else 'OFF'
        s = "{}, name '{}', interval {}s, warnings {}" \
            .format(self.__class__, self.name, self.interval, warning)
        return s

    def _start(self):
        """Start timer (not for public use)."""
        now = time.perf_counter()
        self.start_time = now
        self.target = now + self._interval
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
        self.stop_time = time.perf_counter()
        self.is_stopped = True

    def pause(self):
        """Pause timer immediately, until it is resumed with resume()."""
        # do nothing if timer is already paused (also inactive if timer stopped)
        if not self.is_paused and not self.is_stopped:
            self._bypass_checkpt.set()
            self._unpause_event.clear()
            self._pause_init_time = time.perf_counter()
            self.is_paused = True

    def resume(self):
        """Resume timer after pause event."""
        # do nothing if timer is not paused (also inactive if timer stopped)
        if self.is_paused and not self.is_stopped:
            now = time.perf_counter()
            self._pause_time += now - self._pause_init_time
            self.is_paused = False
            self._unpause_event.set()

    def checkpt(self):
        """Waits at current point in program to keep the interval constant."""

        if self.is_paused:  # if timer is paused, wait for reactivation by resume()

            self._unpause_event.wait()

            # The two lines below (target adjustment and else statement) make
            # the program liberate the checkpt immediately after a pause, and
            # sets the next checkpt one interval away
            self.target = time.perf_counter() + self._interval

        else:

            if not self.interval_exceeded:

                # if time before the previous checkpt has not exceeded the
                # required interval, set target to another multiple of dt

                if self.warnings and self._interval_failed:
                    # only called when interval is ok again after having failed
                    print("--- Time interval ({}s) OK again for {}"
                          .format(self.interval, self.name))
                self._interval_failed = False

                w = self.target - time.perf_counter()
                self.target += self._interval
                self._bypass_checkpt.wait(w)

            else:

                # if already passed target, move on immediately and set target
                # at a time dt from current time to try again.

                if self.warnings and not self._interval_failed:
                    # only called when interval fails right after being ok
                    print("--- Warning, time interval ({}s) too short for {}"
                          .format(self.interval, self.name))
                self._interval_failed = True

                self.target = time.perf_counter() + self.interval

        # always reset the bypass event after a checkpt
        self._bypass_checkpt.clear()

    @property
    def pause_time(self):
        if self.is_paused and not self.is_stopped:
            now = time.perf_counter()
            return self._pause_time + now - self._pause_init_time
        else:
            return self._pause_time

    @property
    def elapsed_time(self):
        """Elapsed time (in s) since last reset or init (if no reset)."""
        t = time.perf_counter() if not self.is_stopped else self.stop_time
        return t - self.start_time - self.pause_time

    @property
    def interval(self):
        """Interval property: time interval of the Timer object."""
        return self._interval

    @interval.setter
    def interval(self, value):
        """Modify existing interval to a new value, effective immediately."""
        self._bypass_checkpt.set()
        self._interval = value
        self.target = time.perf_counter() + value

    @property
    def interval_exceeded(self):
        if time.perf_counter() < self.target:
            return False
        else:
            return True
