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


descr = "GUI countdown clock based on the oclock module."

parser = argparse.ArgumentParser(description=descr,
                                 formatter_class=argparse.RawTextHelpFormatter)

msg = "Input time in hh:mm:ss format, e.g. 10:30:00, or ::5 (5 seconds)"

# The nargs='?' is to have a positional argument with a default value
parser.add_argument('time', type=str, nargs='?', help=msg)

args = parser.parse_args()
countdown = Countdown(args.time)
