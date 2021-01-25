"""GUI for a countdown timer."""

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


import tkinter as tk
from datetime import timedelta

from threading import Thread
from queue import Queue

from . import Timer
from .general import parse_time


# ========================== Appearance parameters ===========================


bgcolor = '#0b3c5d'
textcolor = '#f7f7f7'
donecolor = '#64d253'
overduecolor = '#ff4c4c'


# =========================== Basic clock function ===========================


def clock(timer, total_time, queue):
    """Manage time and calculate remaining time (to be threaded)."""
    while not timer.is_stopped:
        timer.checkpt()
        seconds_remaining = total_time.total_seconds() - timer.elapsed_time
        time_remaining = timedelta(seconds=round(seconds_remaining))
        queue.put(time_remaining)


# =========================== Main Countdown Class ===========================


class Countdown:
    """GUI Countdown timer."""

    def __init__(self, time_str):
        """Init of a Countdown object.

        Input
        -----
        time_str: str (e.g. ::5 for 5 seconds, or 1:30: for 1.5 hours)
        (see oclock.parse_time() for details)
        """
        self.total_time = parse_time(time_str)   # timedelta
        self.timer = Timer(interval=0.2)     # check remaining time every 0.2s

        self.root = tk.Tk()
        self.queue = Queue()  # queue that gets the values of remaining time
        self.done = False

        Thread(target=clock, args=(self.timer, self.total_time, self.queue)).start()
        self.gui()

    def __repr__(self):
        """Str representation of Countdown object"""
        s = "{}, duration {}".format(self.__class__, str(self.total_time))
        return s

# =============================== GUI Methods ================================

    def gui(self):
        """Set up and start GUI."""
        self.root.geometry("150x75")  # Width x Height
        self.root.title("Timer")
        self.root.minsize(170, 40)
        self.root.config(bg=bgcolor)

        self.display = tk.Label(self.root, font=('Helvetica', 30), bg=bgcolor,
                                fg=textcolor, text=str(self.total_time))

        self.display.pack(expand=True)

        self.update()
        self.root.mainloop()
        self.timer.stop()  # run when window closed --> stop program

    def update(self):
        """Define periodic update of GUI."""

        t_remaining = None

        while self.queue.qsize() > 0:
            t_remaining = self.queue.get()

        if t_remaining is not None:

            if t_remaining.total_seconds() > 0:  # ----- timer still counting down
                self.display.config(text=str(t_remaining))

            elif t_remaining.total_seconds() <= -5:  # ------------- timer overdue
                time_str = '- ' + str(-t_remaining)
                self.display.config(text=time_str, fg=overduecolor)

            else:  # ------------------ timer just done (left on screen for 5 sec)
                if not self.done:        # To print only once
                    print('Countdown Finished!')
                    self.display.bell()            # Sound alert
                    self.display.config(text='Done!', fg=donecolor)
                    self.done = True

        self.root.after(100, self.update)  # update every 0.1 seconds
