#! /usr/bin/env python

from __future__ import print_function

"""Guesses if a file is binary or not

Usage:

    binary_guesser <binary file>

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
from bio_utils.verifiers import FormatError
import string
import sys

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '2.0.1'
__credits__ = 'Andrew Dalke'


# Credit: http://code.activestate.com/
# recipes/173220-test-if-a-file-or-string-is-text-or-binary/
def binary_guesser(handle, bytes=512):
    """Raise error if file not likely binary

    Guesses if a file is binary, raises error if file is not likely binary,
    then returns to location in file when handle passed to binary_guesser.

    Args:
        handle (file): File handle of file thought to be binary

        bytes (int): Bytes of file to read to guess binary, more bytes
            is often better but takes longer

    Raises:
        FormatError: Error raised if file is not likely binary

    Example:
        The following example demonstrate how to use binary_guesser.
        Note: These doctests will not pass, examples are only in doctest
        format as per convention. bio_utils uses pytests for testing.

        >>> binary_guesser(open('test.binary'))
    """

    text_characters = ''.join(map(chr, range(32, 127))) + '\n\r\t\b'
    null_trans = string.maketrans("", "")
    handle_location = handle.tell()
    first_block = handle.read(bytes)
    filtered_block = first_block.translate(null_trans, text_characters)
    handle.seek(handle_location)  # Return to original handle location
    if float(len(filtered_block)) / float(len(first_block)) > 0.30:
        pass  # File is likely binary
    else:
        msg = '{0} is probably not a binary file'.format(handle.name)
        raise FormatError(message=msg)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('binary',
                        help='file to verify if binary [Default: STDIN]',
                        type=argparse.FileType('rU'),
                        default=sys.stdin)
    parser.add_argument('-q', '--quiet',
                        help='Suppresses output when file is good',
                        action='store_false')
    args = parser.parse_args()

    binary_guesser(args.binary)
    if not args.quiet:
        print('{} is probably a binary file'.format(args.binary.name))


if __name__ == '__main__':
    main()
    sys.exit(0)
