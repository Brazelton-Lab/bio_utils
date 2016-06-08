#! /usr/bin/env python

from __future__ import print_function

"""Writes lines from the B6/M8 file under the given E-value to output

Usage:

    b6_evalue_filter.py --b6 <b6 file> --e_value <max e_value>
                        --output <output file>

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
__version__ = '2.0.0'


def b6_evalue_filter(handle, e_value, *args, **kwargs):
    """Yields lines from handle with E-value less than or equal to e_value

    Args:
        handle (file): B6/M8 file handle, can be any iterator so long as it
            it returns subsequent "lines" of a B6/M8 entry

        e_value (float): max E-value to return

        *args: Variable length argument list for b6_iter

        **kwargs: Arbitrary keyword arguments for b6_iter

    Yields:
        B6Entry: class containing all B6/M8 data

    Example:
        Note: These doctests will not pass, examples are only in doctest
        format as per convention. bio_utils uses pytests for testing.

        >>> b6_handle = open('test.b6')
        >>> for entry in b6_evalue_filter(b6_handle, 1e5)
        ...     print(entry.evalue)  # Print E-value of filtered entry
    """

    for entry in b6_iter(handle, *args, **kwargs):
        if entry.evalue <= e_value:
            yield entry


def main():
    """Open B6/M8 file, filter entries by E-Value, and write said entries"""

    for entry in b6_evalue_filter(args.b6, args.e_value):
        args.output.write(entry.write())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('-b', '--b6',
                        nargs='?',
                        type=argparse.FileType('rU'),
                        default=sys.stdin,
                        help='M8 (B6 in BLAST+) file with alignment data'
                             '[Default: STDIN]')
    parser.add_argument('-e', '--e_value',
                        type=float,
                        help='upper E-Value cutoff')
    parser.add_argument('-o', '--output',
                        nargs='?',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='optional output file [Default: STDOUT]')
    args = parser.parse_args()

    main()
    sys.exit(0)
