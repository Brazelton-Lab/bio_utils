#!/usr/bin/env python

from __future__ import print_function

"""Verifies a FASTA file

Usage:

    fasta_verifier <FASTA file>

Copyright:

    fasta.py verify validity of a FASTA file
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
from bio_utils.iterators import fasta_iter
from bio_utils.verifiers import entry_verifier
from bio_utils.verifiers import FormatError
import os
import sys

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Beta'
__version__ = '2.0.0'


# noinspection PyTypeChecker
def fasta_verifier(entries, ambiguous=False):
    """Returns True if FASTA entry is valid, else False

    Args:
        entries (list): A list of FastaEntry objects

        ambiguous (bool): Permit ambiguous bases, i.e. permit non-ACGTU bases

    Raises:
        FormatError: Error when FASTA format incorrect with descriptive message
    """

    if ambiguous:
        regex = r'^>.+{0}[ACGTURYKMSWBDHVNX]+{0}$'.format(os.linesep)
    else:
        regex = r'^>.+{0}[ACGTU]+{0}$'.format(os.linesep)
    delimiter = r'{0}'.format(os.linesep)
    for entry in entries:
        try:
            entry_verifier([entry.write()], regex, delimiter)
        except FormatError as err:
            if err.part == 0:
                msg = 'Unknown Header Error with {0}'.format(entry.id)
                raise FormatError(message=msg)
            elif err.part == 1 and ambiguous:
                msg = '{0} contains a base not in ' \
                      '[ACGTURYKMSWBDHVNX]'.format(entry.id)
                raise FormatError(message=msg)
            elif err.part == 1 and not ambiguous:
                msg = '{0} contains a base not in ' \
                      '[ACGTU]'.format(entry.id)
                raise FormatError(message=msg)
            else:
                msg = 'Unknown Error: Likely a Bug'
                raise FormatError(message=msg)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('fasta',
                        help='FASTA file to verify, Default: STDIN',
                        type=argparse.FileType('rU'),
                        default=sys.stdin)
    args = parser.parse_args()

    for entry in fasta_iter(args.fasta):
        fasta_verifier(entry)
    print('{0} is valid'.format(args.fasta.name))


if __name__ == '__main__':
    main()
    sys.exit(0)
