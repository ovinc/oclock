"""GUI for a countdown timer."""

import tkinter as tk
from datetime import timedelta

from threading import Thread, Event
from queue import Queue

from . import Timer
from .general import parse_time


# ========================== Appearance parameters ===========================

bgcolor = '#0b3c5d'
textcolor = '#f7f7f7'
donecolor = '#64d253'
overduecolor = '#ff4c4c'

# =========================== Secondary functions ============================

def remaining_time(total_time, timer, e_stop, q_time):
    """Manages time and calculate remaining time

    total_time is a timedelta
    timer is a timer object from the oclock module
    q_time is a queue that gets the values of remaining time
    e_stop is an event that exits the program when set
    """
    t_remaining = total_time
    timer.reset()

    while not e_stop.is_set():

        timer.checkpt()

        t_remaining -= timedelta(seconds=1)
        q_time.put(t_remaining)


def update(root, display, q_time):
    """Define periodic update of GUI."""

    t_remaining = None

    while q_time.qsize() > 0:
        t_remaining = q_time.get()

    if t_remaining is not None:

        if t_remaining.total_seconds() > 0:  # ----- timer still counting down
            display.config(text=str(t_remaining))

        elif t_remaining.total_seconds() <= -5:  # ------------- timer overdue
            time_str = '- ' + str(-t_remaining)
            display.config(text=time_str, fg=overduecolor)

        else:  # ------------------ timer just done (left on screen for 5 sec)
            print('\aCountdown Finished!')  # \a is to play sound alert
            display.config(text='Done!', fg=donecolor)

    root.after(100, update, root, display, q_time)  # update every 0.1 seconds


def gui(total_time, q_time, e_stop):
    """Set up and start GUI."""

    root = tk.Tk()

    root.geometry("150x75")  # Width x Height
    root.title("Timer")
    root.minsize(120, 40)
    root.config(bg=bgcolor)

    display = tk.Label(root, font=('Helvetica', 30), bg=bgcolor, fg=textcolor,
                       text=str(total_time))

    display.pack(expand=True)

    update(root, display, q_time)
    root.mainloop()

    e_stop.set()


# ============================== MAIN FUNCTION ===============================


def countdown(time_str):
    """Run the timer and the GUI concurrently.

    Input
    -----
    time_str: str (e.g. ::5 for 5 seconds, or 1:30: for 1.5 hours)
    (see oclock.parse_time() for details)
    """
    total_time = parse_time(time_str)

    timer = Timer(interval=1)

    q_time = Queue()
    e_stop = Event()

    Thread(target=remaining_time, args=(total_time, timer, e_stop, q_time)).start()
    gui(total_time, q_time, e_stop)
