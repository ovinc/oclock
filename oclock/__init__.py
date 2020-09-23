"""Cancellable timer for loops of constant duration."""

# TODO: make pause() and restart() interact with checkpt() (pauses loop)

from .timer import Timer
from .countdown import countdown
from .general import parse_time

__version__ = 1.0
