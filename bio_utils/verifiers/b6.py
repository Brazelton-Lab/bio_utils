#!/usr/bin/env python

"""Verifies a B6/M8 file

Usage:

    b6_verifier <b6File>

Copyright:

    b6.py verify validity of a B6/M8 file
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
from bio_utils.verifiers.line_verifier import verify_lines
from bio_utils.iterators import b6_iter
import sys

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.2.2'


def b6_verifier(handle):
    """Returns True if B6/M8 file is valid and False if file is not valid

    :param handle: B6/M8 file handle
    :type handle: File Object
    """

    lines = []
    for entry in b6_iter(handle):
        lines.append(entry.write())
    regex = r'^.+\t.+\t\d+\.?\d*\t\d+\t\d+\t\d+\t\d+\t\d+\t\d+\t\d+\t' \
            + r'\d+\.?\d*(e-)?\d*\t\d+\.?\d*\n$'
    delimiter = r'\t'
    m8_status = verify_lines(lines, regex, delimiter)
    return m8_status


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('b6File',
                        help='B6/M8 file to verify')
    args = parser.parse_args()

    with open(args.b6File, 'rU') as in_handle:
        valid = b6_verifier(in_handle)
    if valid:
        print('{} is valid'.format(args.b6File))
    else:
        print('{} is not valid'.format(args.b6File))


if __name__ == '__main__':
    main()
    sys.exit(0)
