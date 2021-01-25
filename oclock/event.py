"""Custom class mimicking threading Event, but with better timing accuracy.

Originally written by Chris D. and posted on StackOverflow:
https://stackoverflow.com/questions/48984512/making-a-timer-timeout-inaccuracy-of-threading-event-wait-python-3-6

The olock package is licensed under GNU GPLv3 that is compatible with
StackOverflow's CC BY-SA 4.0 license."""

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
import _thread
import datetime


class Event:
    __slots__ = (
        "_flag", "_lock", "_nl",
        "_pc", "_waiters"
    )

    _lock_type = _thread.LockType
    _timedelta = datetime.timedelta
    _perf_counter = time.perf_counter
    _new_lock = _thread.allocate_lock

    class _switch:
        __slots__ = ("_on",)

        def __call__(self, on: bool = None):
            if on is None:
                return self._on

            self._on = on

        def __bool__(self):
            return self._on

        def __init__(self):
            self._on = False

    def clear(self):
        with self._lock:
            self._flag(False)

    def is_set(self) -> bool:
        return self._flag()

    def set(self):
        with self._lock:
            self._flag(True)
            waiters = self._waiters

            for waiter in waiters:
                waiter.release()

            waiters.clear()

    def wait(
        self,
        timeout: float = None
    ) -> bool:
        with self._lock:
            return self._wait(self._pc(), timeout)

    def _new_waiter(self) -> _lock_type:
        waiter = self._nl()
        waiter.acquire()
        self._waiters.append(waiter)
        return waiter

    def _wait(
        self,
        start: float,
        timeout: float,
        td=_timedelta,
        pc=_perf_counter,
        end: _timedelta = None,
        waiter: _lock_type = None,
        new_thread=_thread.start_new_thread,
        thread_delay=_timedelta(milliseconds=3)
    ) -> bool:
        flag = self._flag

        if flag:
            return True
        elif timeout is None:
            waiter = self._new_waiter()
        elif timeout <= 0:
            return False
        else:
            delay = td(seconds=timeout)
            end = td(seconds=start) + delay

            if delay > thread_delay:
                mark = end - thread_delay
                waiter = self._new_waiter()
                new_thread(
                    self._wait_thread,
                    (flag, mark, waiter)
                )

        lock = self._lock
        lock.release()

        try:
            if waiter:
                waiter.acquire()

            if end:
                while (
                    not flag and
                    td(seconds=pc()) < end
                ):
                    pass

        finally:
            lock.acquire()

            if waiter and not flag:
                self._waiters.remove(waiter)

        return flag()

    @staticmethod
    def _wait_thread(
        flag: _switch,
        mark: _timedelta,
        waiter: _lock_type,
        td=_timedelta,
        pc=_perf_counter,
        sleep=time.sleep
    ):
        while not flag and td(seconds=pc()) < mark:
            sleep(0.001)

        if waiter.locked():
            waiter.release()

    def __new__(cls):
        _new_lock = cls._new_lock
        _self = object.__new__(cls)
        _self._waiters = []
        _self._nl = _new_lock
        _self._lock = _new_lock()
        _self._flag = cls._switch()
        _self._pc = cls._perf_counter
        return _self


if __name__ == "__main__":
    def test_wait_time():
        wait_time = datetime.timedelta(microseconds=1)
        wait_time = wait_time.total_seconds()

        def test(
            event=Event(),
            delay=wait_time,
            pc=time.perf_counter
        ):
            pc1 = pc()
            event.wait(delay)
            pc2 = pc()
            pc1, pc2 = [
                int(nbr * 1000000000)
                for nbr in (pc1, pc2)
            ]
            return pc2 - pc1

        lst = [
            f"{i}.\t\t{test()}"
            for i in range(1, 11)
        ]
        print("\n".join(lst))

    test_wait_time()
    del test_wait_time
