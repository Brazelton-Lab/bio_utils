#!/usr/bin/env python

from __future__ import print_function

"""Guesses if a file is binary or not

Usage:

    binary_verifier <binaryFile>

Copyright:

    binary.py guess if file is binary
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
import string
import sys

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.2.2'
__credits__ = 'Andrew Dalke'


# Credit: http://code.activestate.com/
# recipes/173220-test-if-a-file-or-string-is-text-or-binary/
def binary_verifier(handle):
    """Returns True if file is probably binary and False if not

    :param handle: Binary file handle
    :type handle: File Object
    """

    text_characters = ''.join(map(chr, range(32, 127)) + list('\n\r\t\b'))
    null_trans_table = string.maketrans('', '')
    first_block = handle.read(512)
    filtered_block = first_block.translate(null_trans_table, text_characters)
    if float(len(filtered_block)) / float(len(first_block)) > 0.30:
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('binaryFile',
                        help='file to verify if binary')
    args = parser.parse_args()

    with open(args.binaryFile, 'rU') as in_handle:
        valid = binary_verifier(in_handle)
    if valid:
        print('{} is probably a binary file'.format(args.binaryFile))
    else:
        print('{} is probably a binary file'.format(args.binaryFile))


if __name__ == '__main__':
    main()
    sys.exit(0)
