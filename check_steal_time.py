#!/usr/bin/env python
#
# InnoGames Monitoring Plugins - check_steal_time.py
#
# This script checks the steal time of all vCPUs on the regarding domain and
# raises a warning or critical state if a reasonable threshold is reached.
# Values for the warning and critical thresholds can be specified using
# parameters.
#
# Copyright (c) 2017, InnoGames GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from argparse import ArgumentParser
import subprocess
from sys import exit
import re


def main():
    """Main entrypoint for script"""

    args = get_parser().parse_args()

    steal = float(get_steal_time())

    code = 0

    if steal > args.critical:
        status = 'CRITICAL'
        code = 2
    elif steal > args.warning:
        status = 'WARNING'
        code = 1
    else:
        status = 'OK'

    print('{} - Steal time value is {}%'.format(status, steal))

    exit(code)


def get_parser():
    """Get argument parser -> ArgumentParser"""

    parser = ArgumentParser()

    parser.add_argument(
        '--warning', '-w', help='warning threshold for steal time',
        default=50
    )
    parser.add_argument(
        '--critical', '-c', help='critical threshold for steal time',
        default=75
    )

    return parser


def get_steal_time():
    """Get the actual steal time of the host"""

    output = subprocess.check_output('iostat -c', shell=True)
    output = output.split()
    steal = output[18].replace(',', '.')

    return steal


if __name__ == '__main__':
    main()
