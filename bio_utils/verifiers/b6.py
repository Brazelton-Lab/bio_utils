#!/usr/bin/env python

from __future__ import print_function

"""Verifies a B6/M8 file

Usage:

    b6_verifier <B6 file> [--quiet]

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
from bio_utils.iterators import b6_iter
from bio_utils.verifiers import entry_verifier
from bio_utils.verifiers import FormatError
import os
import sys

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Alpha'
__version__ = '2.0.0'


def b6_verifier(entries, line=None):
    """Raises error if invalid B6/M8 format detected

    Args:
        entries (list): A list of B6Entry objects

        line (int): Line number of first entry

    Raises:
        FormatError: Error when B6/M8 format incorrect with descriptive message

    Example:
        >>> from bio_utils.iterators import b6_iter
        >>> import os
        >>> entries = 'query1\tsubject1\t86.03\t1782\t226\t18\t6038\t7812\t' \
        ...           '755762\t753997\t0.0\t1890{0}' \
        ...           'query2\tsubject2\t85.46\t1176\t165\t5\t1213\t2385\t' \
        ...           '1154754\t1153582\t0.0\t1219'.format(os.linesep)
        >>> b6_entries = b6_iter(iter(entries.split(os.linesep)))
        >>> b6_verifier(b6_entries)
    """

    if type(entries) is str:  # Convert single str entries to lists
        entries = [entries]
    regex = r'^.+\t.+\t\d+\.?\d*\t\d+\t\d+\t\d+\t\d+\t\d+\t\d+\t\d+\t' \
            + r'\d+\.?\d*(e-)?\d*\t\d+\.?\d*{0}$'.format(os.linesep)
    delimiter = r'\t'

    for entry in entries:
        try:
            entry_verifier([entry.write()], regex, delimiter)
        except FormatError as error:
            if line:
                if error.part == 0:
                    msg = 'Line {0} has no query ID'.format(str(line))
                    raise FormatError(message=msg)
                elif error.part == 1:
                    msg = 'Line {0} has no subject ID'.format(str(line))
                    raise FormatError(message=msg)
                elif error.part == 2:
                    msg = 'Line {0} has non-numerical ' \
                          'characters in percent identity'.format(str(line))
                    raise FormatError(message=msg)
                elif error.part == 3:
                    msg = 'Line {0} has non-numerical ' \
                          'characters in alignment length'.format(str(line))
                    raise FormatError(message=msg)
                elif error.part == 4:
                    msg = 'Line {0} has non-numerical ' \
                          'characters in mismatches'.format(str(line))
                    raise FormatError(message=msg)
                elif error.part == 5:
                    msg = 'Line {0} has non-numerical ' \
                          'characters in gaps'.format(str(line))
                    raise FormatError(message=msg)
                elif error.part == 6:
                    msg = 'Line {0} has non-numerical ' \
                          'characters in query start'.format(str(line))
                    raise FormatError(message=msg)
                elif error.part == 7:
                    msg = 'Line {0} has non-numerical ' \
                          'characters in query end'.format(str(line))
                    raise FormatError(message=msg)
                elif error.part == 8:
                    msg = 'Line {0} has non-numerical ' \
                          'characters in subject start'.format(str(line))
                    raise FormatError(message=msg)
                elif error.part == 9:
                    msg = 'Line {0} has non-numerical ' \
                          'characters in subject end'.format(str(line))
                    raise FormatError(message=msg)
                elif error.part == 10:
                    msg = 'Line {0} has non-numerical ' \
                          'characters in E-value'.format(str(line))
                    raise FormatError(message=msg)
                elif error.part == 11:
                    msg = 'Line {0} has non-numerical ' \
                          'characters in bit score'.format(str(line))
                    raise FormatError(message=msg)
                else:
                    msg = 'Unknown Error: Likely a Bug'
                    raise FormatError(message=msg)
            else:
                if error.part == 0:
                    msg = 'An entry with subject ID {0} ' \
                          'has no query ID'.format(entry.subject)
                    raise FormatError(message=msg)
                elif error.part == 1:
                    msg = 'An entry with query ID {0} ' \
                          'has no subject ID'.format(entry.query)
                    raise FormatError(message=msg)
                elif error.part == 2:
                    msg = 'An entry with query ID {0} has non-numerical ' \
                          'characters in percent identity'.format(entry.query)
                    raise FormatError(message=msg)
                elif error.part == 3:
                    msg = 'An entry with query ID {0} has non-numerical ' \
                          'characters in alignment length'.format(entry.query)
                    raise FormatError(message=msg)
                elif error.part == 4:
                    msg = 'An entry with query ID {0} has non-numerical ' \
                          'characters in mismatches'.format(entry.query)
                    raise FormatError(message=msg)
                elif error.part == 5:
                    msg = 'An entry with query ID {0} has non-numerical ' \
                          'characters in gaps'.format(entry.query)
                    raise FormatError(message=msg)
                elif error.part == 6:
                    msg = 'An entry with query ID {0} has non-numerical ' \
                          'characters in query start'.format(entry.query)
                    raise FormatError(message=msg)
                elif error.part == 7:
                    msg = 'An entry with query ID {0} has non-numerical ' \
                          'characters in query end'.format(entry.query)
                    raise FormatError(message=msg)
                elif error.part == 8:
                    msg = 'An entry with query ID {0} has non-numerical ' \
                          'characters in subject start'.format(entry.query)
                    raise FormatError(message=msg)
                elif error.part == 9:
                    msg = 'An entry with query ID {0} has non-numerical ' \
                          'characters in subject end'.format(entry.query)
                    raise FormatError(message=msg)
                elif error.part == 10:
                    msg = 'An entry with query ID {0} has non-numerical ' \
                          'characters in E-value'.format(entry.query)
                    raise FormatError(message=msg)
                elif error.part == 11:
                    msg = 'An entry with query ID {0} has non-numerical ' \
                          'characters in bit score'.format(entry.query)
                    raise FormatError(message=msg)
                else:
                    msg = 'Unknown Error: Likely a Bug'
                    raise FormatError(message=msg)

        if line:
            line += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('b6',
                        help='B6/M8 file to verify [Default: STDIN]',
                        type=argparse.FileType('rU'),
                        default=sys.stdin)
    parser.add_argument('-q', '--quiet',
                        help='Suppresses positive message when  file is good',
                        action='store_false')
    args = parser.parse_args()

    for entry in b6_iter(args.b6):
        b6_verifier(entry)
    if not args.quiet:
        print('{0} is valid').format(args.b6.name)


if __name__ == '__main__':
    main()
    sys.exit(0)
