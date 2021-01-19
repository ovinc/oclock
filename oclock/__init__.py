"""Timing tools, including cancellable timers for loops of constant duration."""

from .timer import Timer
from .countdown import Countdown
from .general import parse_time, measure_time, measure_duration
from .loop import loop, interactiveloop

# from importlib.metadata import version (only for python 3.8+)
from importlib_metadata import version

__version__ = version('oclock')
__author__ = 'Olivier Vincent'
__license__ = '3-Clause BSD'