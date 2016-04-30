#! /usr/bin/env python

from __future__ import print_function

"""Writes lines from the B6/M8 file under the given e-value to output

Usage:

    b6_evalue_filter.py --b6_file [b6_file] --e_value [e_value]
                        --output [output]

Copyright:

    filter_b6_evalue.py filter lines of B6/M8 file by e-value
    Copyright (C) 2015  William Brazelton, Alex Hyer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
from bio_utils.iterators import b6_iter
import sys

__author__ = 'William Brazelton, Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.1.3'


def b6_evalue_filter(handle, e_value):
    """Returns lines from handle with e-value less than or equal to e_value

    :returns: yields B6/M8 entries below e-value cutoff
    :rtype: dict

    :param handle: file handle of M8 file
    :type handle: file object

    :param e_value: upper e-value threshold
    :type e_value: float
    """

    for entry in b6_iter(handle):
        if float(entry.evalue) <= e_value:
            yield entry


def main():
    with open(args.b6_file, 'rU') as b6_handle:
        for entry in b6_evalue_filter(b6_handle, args.e_value):
            args.output.write(entry.write())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('-m', '--b6_file',
                        nargs='?',
                        type=argparse.FileType('rU'),
                        default=sys.stdin,
                        help='M8 (B6 in BLAST+) file with alignment data'
                             '[Default: STDIN]')
    parser.add_argument('-e', '--e_value',
                        type=float,
                        help='upper e-value cutoff')
    parser.add_argument('-o', '--output',
                        nargs='?',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='optional output file [Default: STDOUT]')
    args = parser.parse_args()

    main()
    sys.exit(0)
