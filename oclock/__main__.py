"""Manage command line parsing for the oclock module."""

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

import argparse

from .countdown import Countdown


description = (
    "GUI countdown clock based on the oclock module.\n\n"
    "Examples\n"
    "--------\n"
    "Timer for 5 seconds:\n"
    ">>> python -m oclock ::5\n\n"
    "Timer for 1 hour and 25 minutes:\n"
    ">>> python -m oclock 1:25:\n"
)

parser = argparse.ArgumentParser(
    description=description,
    formatter_class=argparse.RawTextHelpFormatter,
    prog='python -m oclock',
)

msg = (
    "Duration in hh:mm:ss format, e.g. "
    "1:25:30 (1 hour, 25 min and 30 seconds), "
    "or ::5 (5 seconds)."
)

parser.add_argument("time", type=str, help=msg)

args = parser.parse_args()
countdown = Countdown(args.time)
