#!/usr/bin/env python

from __future__ import print_function

"""Verifies a SAM file

Usage:

    sam_verifier <samFile>

Copyright:

    sam.py verify validity of a SAM file
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
from bio_utils.iterators import sam_iter
import sys

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.1.3'


def sam_verifier(handle):
    """Returns True if SAM file is valid and False if file is not valid

    :param handle: SAM file handle
    :type handle: File Object
    """

    lines = []
    for entry in sam_iter(handle):
        lines.append(entry.write())
    regex = r'^[!-?A-~]{1,255}\t' \
            + r'([0-9]{1,4}|[0-5][0-9]{4}|' \
            + r'[0-9]{1,4}|[1-5][0-9]{4}|' \
            + r'6[0-4][0-9]{3}|65[0-4][0-9]{2}|' \
            + r'655[0-2][0-9]|6553[0-7])\t' \
            + r'\*|[!-()+-<>-~][!-~]*\t' \
            + r'([0-9]{1,9}|1[0-9]{9}|2(0[0-9]{8}|' \
            + r'1([0-3][0-9]{7}|4([0-6][0-9]{6}|' \
            + r'7([0-3][0-9]{5}|4([0-7][0-9]{4}|' \
            + r'8([0-2][0-9]{3}|3([0-5][0-9]{2}|' \
            + r'6([0-3][0-9]|4[0-7])))))))))\t' \
            + r'([0-9]{1,2}|1[0-9]{2}|' \
            + r'2[0-4][0-9]|25[0-5])\t' \
            + r'\*|([0-9]+[MIDNSHPX=])+\t' \
            + r'\*|=|[!-()+-<>-~][!-~]*\t' \
            + r'([0-9]{1,9}|1[0-9]{9}|2(0[0-9]{8}|' \
            + r'1([0-3][0-9]{7}|4([0-6][0-9]{6}|' \
            + r'7([0-3][0-9]{5}|4([0-7][0-9]{4}|' \
            + r'8([0-2][0-9]{3}|3([0-5][0-9]{2}|' \
            + r'6([0-3][0-9]|4[0-7])))))))))\t' \
            + r'-?([0-9]{1,9}|1[0-9]{9}|2(0[0-9]{8}|' \
            + r'1([0-3][0-9]{7}|4([0-6][0-9]{6}|' \
            + r'7([0-3][0-9]{5}|4([0-7][0-9]{4}|' \
            + r'8([0-2][0-9]{3}|3([0-5][0-9]{2}|' \
            + r'6([0-3][0-9]|4[0-7])))))))))\t' \
            + r'\*|[A-Za-z=.]+\t' \
            + r'[!-~]+\n$'
    delimiter = r'\t'
    sam_status = verify_lines(lines, regex, delimiter)
    return sam_status


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse. \
                                     RawDescriptionHelpFormatter)
    parser.add_argument('samFile',
                        help='SAM file to verify')
    args = parser.parse_args()

    with open(args.samFile, 'rU') as in_handle:
        valid = sam_verifier(in_handle)
    if valid:
        print('{} is valid'.format(args.samFile))
    else:
        print('{} is not valid'.format(args.samFile))


if __name__ == '__main__':
    main()
    sys.exit(0)
