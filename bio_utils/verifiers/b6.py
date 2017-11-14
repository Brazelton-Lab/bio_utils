#! /usr/bin/env python

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
__status__ = 'Production'
__version__ = '2.1.3'


def b6_verifier(entries, line=None):
    """Raises error if invalid B6/M8 format detected

    Args:
        entries (list): A list of B6Entry instances

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

    regex = r'^.+\t.+\t\d+\.?\d*\t\d+\t\d+\t\d+\t\d+\t\d+\t\d+\t\d+\t' \
            + r'\d+\.?\d*(e-)?\d*\t\d+\.?\d*{0}$'.format(os.linesep)
    delimiter = r'\t'

    for entry in entries:
        try:
            entry_verifier([entry.write()], regex, delimiter)
        except FormatError as error:
            # Format info on what entry error came from
            if line:
                intro = 'Line {0}'.format(str(line))
            elif error.part == 0:
                intro = 'Entry with subject ID {0}'.format(entry.subject)
            else:
                intro = 'Entry with query ID {0}'.format(entry.query)

            # Generate error
            if error.part == 0:
                msg = '{0} has no query ID'.format(intro)
            elif error.part == 1:
                msg = '{0} has no subject ID'.format(intro)
            elif error.part == 2:
                msg = '{0} has non-numerical ' \
                      'characters in percent identity'.format(intro)
            elif error.part == 3:
                msg = '{0} has non-numerical ' \
                      'characters in alignment length'.format(intro)
            elif error.part == 4:
                msg = '{0} has non-numerical ' \
                      'characters in mismatches'.format(intro)
            elif error.part == 5:
                msg = '{0} has non-numerical ' \
                      'characters in gaps'.format(intro)
            elif error.part == 6:
                msg = '{0} has non-numerical ' \
                      'characters in query start'.format(intro)
            elif error.part == 7:
                msg = '{0} has non-numerical ' \
                      'characters in query end'.format(intro)
            elif error.part == 8:
                msg = '{0} has non-numerical ' \
                      'characters in subject start'.format(intro)
            elif error.part == 9:
                msg = '{0} has non-numerical ' \
                      'characters in subject end'.format(intro)
            elif error.part == 10:
                msg = '{0} has non-numerical ' \
                      'characters in E-value'.format(intro)
            elif error.part == 11:
                msg = '{0} has non-numerical ' \
                      'characters in bit score'.format(intro)
            else:
                msg = '{0}: Unknown Error: Likely a Bug'.format(intro)
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
                        help='Suppresses message when file is good',
                        action='store_false')
    args = parser.parse_args()

    for entry in enumerate(b6_iter(args.b6)):
        b6_verifier([entry[1]], line=entry[0]+1)
    if not args.quiet:
        print('{0} is valid').format(args.b6.name)


if __name__ == '__main__':
    main()
    sys.exit(0)
