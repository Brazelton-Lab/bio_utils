#! /usr/bin/env python

from __future__ import print_function

"""Verifies a FASTQ file

Usage:

    fastq_verifier <FASTQ File> [--quiet]

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
from bio_utils.iterators import fastq_iter
from bio_utils.verifiers import entry_verifier
from bio_utils.verifiers import FormatError
import os
import sys

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '2.0.2'


# noinspection PyTypeChecker
def fastq_verifier(entries, ambiguous=False):
    """Raises error if invalid FASTQ format detected

    Args:
        entries (list): A list of FastqEntry instances

        ambiguous (bool): Permit ambiguous bases, i.e. permit non-ACGTU bases

    Raises:
        FormatError: Error when FASTQ format incorrect with descriptive message

    Example:
        >>> from bio_utils.iterators import fastq_iter
        >>> import os
        >>> entries = r'@entry1{0}AAGGATTCG{0}+{0}112234432{0}' \
        ...           r'@entry{0}AGGTCCCCCG{0}+{0}4229888884{0}' \
        ...           r'@entry3{0}GCCTAGC{0}9ddsa5n'.format(os.linesep)
        >>> fastq_entries = fastq_iter(iter(entries.split(os.linesep)))
        >>> fastq_verifier(fastq_entries)
    """

    if ambiguous:
        regex = r'^@.+{0}[ACGTURYKMSWBDHVNX]+{0}' \
                r'\+.*{0}[!"#$%&\'()*+,-./0123456' \
                r'789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                r'[\]^_`abcdefghijklmnopqrstuvwxyz' \
                r'{{|}}~]+{0}$'.format(os.linesep)
    else:
        regex = r'^@.+{0}[ACGTU]+{0}' \
                r'\+.*{0}[!-~]+{0}$'.format(os.linesep)
    delimiter = r'{0}'.format(os.linesep)

    for entry in entries:
        if len(entry.sequence) != len(entry.quality):
            msg = 'The number of bases in {0} does not match the number ' \
                  'of quality scores'.format(entry.id)
            raise FormatError(message=msg)
        try:
            entry_verifier([entry.write()], regex, delimiter)
        except FormatError as error:
            if error.part == 0:
                msg = 'Unknown Header Error with {0}'.format(entry.id)
                raise FormatError(message=msg)
            elif error.part == 1 and ambiguous:
                msg = '{0} contains a base not in ' \
                      '[ACGTURYKMSWBDHVNX]'.format(entry.id)
                raise FormatError(message=msg)
            elif error.part == 1 and not ambiguous:
                msg = '{0} contains a base not in ' \
                      '[ACGTU]'.format(entry.id)
                raise FormatError(message=msg)
            elif error.part == 2:
                msg = 'Unknown error with line 3 of {0}'.format(entry.id)
                raise FormatError(message=msg)
            elif error.part == 3:
                msg = r'{0} contains a quality score not in ' \
                      r'[!-~]'.format(entry.id)
                raise FormatError(message=msg)
            else:
                msg = '{0}: Unknown Error: Likely a Bug'.format(entry.id)
                raise FormatError(message=msg)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('fastq',
                        help='FASTQ file to verify [Default: STDIN]',
                        type=argparse.FileType('rU'),
                        default=sys.stdin)
    parser.add_argument('-q', '--quiet',
                        help='Suppresses message when file is good',
                        action='store_false')
    args = parser.parse_args()

    for entry in fastq_iter(args.fasta):
        fastq_verifier([entry])
    if not args.quiet:
        print('{0} is valid'.format(args.fastq.name))  # Prints if no error


if __name__ == '__main__':
    main()
    sys.exit(0)
