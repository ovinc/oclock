"""Timing tools, including cancellable timers for loops of constant duration."""

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


from .timer import Timer
from .countdown import Countdown
from .general import parse_time, measure_time, measure_duration, after
from .loop import loop, interactiveloop
from .event import Event

# from importlib.metadata import version (only for python 3.8+)
from importlib_metadata import version

__version__ = version('oclock')
__author__ = 'Olivier Vincent'
__license__ = 'GNU GPLv3'
