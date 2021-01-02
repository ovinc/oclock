"""Manage command line parsing for the oclock module."""

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
