#!/usr/bin/env python

from __future__ import print_function

"""Verifies a FASTQ file

Usage:

    fastq_verifier <fastqFile>

Copyright:

    fastq.py verify validity of a FASTQ file
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
from bio_utils.iterators import fastq_iter
import sys

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.2.2'


# noinspection PyTypeChecker
def fastq_verifier(handle):
    """Returns True if FASTQ file is valid and False if file is not valid

    :param handle: FASTQ file handle
    :type handle: File Object
    """

    lines = []
    for entry in fastq_iter(handle):
        lines.append(entry.write())
    regex = r'^@.+\n[ACGTURYKMSWBDHVNX]+\n\+.*\n.+\n$'
    delimiter = r'\n'
    fastq_status = verify_lines(lines, regex, delimiter)
    return fastq_status


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('fastqFile',
                        help='FASTQ file to verify')
    args = parser.parse_args()

    with open(args.fastqFile, 'rU') as in_handle:
        valid = fastq_verifier(in_handle)
    if valid:
        print('{} is valid'.format(args.fastqFile))
    else:
        print('{} is not valid'.format(args.fastqFile))


if __name__ == '__main__':
    main()
    sys.exit(0)
