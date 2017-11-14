#! /usr/bin/env python

from __future__ import print_function

"""Verifies a SAM file

Usage:

    sam_verifier <SAM file> [--quiet]

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
from bio_utils.verifiers import entry_verifier
from bio_utils.verifiers import FormatError
from bio_utils.iterators import sam_iter
import os
import sys

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '2.0.0'


def sam_verifier(entries, line=None):
    """Raises error if invalid SAM format detected

    Args:
        entries (list): A list of SamEntry instances

        line (int): Line number of first entry

    Raises:
        FormatError: Error when SAM format incorrect with descriptive message
    """

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
            + r'[!-~]+{0}$'.format(os.linesep)
    delimiter = r'\t'

    for entry in entries:
        try:
            entry_verifier([entry.write()], regex, delimiter)
        except FormatError as error:
            # Format info on what entry error came from
            if line:
                intro = 'Line {0}'.format(str(line))
            elif error.part == 0:
                intro = 'An entry with reference {0}'.format(entry.rname)
            else:
                intro = 'An entry with query {0}'.format(entry.qname)

            # Generate error
            if error.part == 0:
                if len(entry.qname) == 0:
                    msg = '{0} has no query name'.format(intro)
                elif len(entry.qname) > 255:
                    msg = '{0} query name must be less than 255 ' \
                          'characters'.format(intro)
                else:
                    msg = '{0} query name contains characters not in ' \
                          '[!-?A-~]'.format(intro)
            elif error.part == 1:
                msg = '{0} flag not in range [0-(2^31-1)]'.format(intro)
            elif error.part == 2:
                if len(entry.rname) == 0:
                    msg = '{0} has no reference name'.format(intro)
                else:
                    msg = '{0} reference name has characters not in ' \
                          '[!-()+-<>-~][!-~]'.format(intro)
            elif error.part == 3:
                msg = '{0} leftmost position not in range ' \
                      '[0-(2^31-1)]'.format(intro)
            elif error.part == 4:
                msg = '{0} mapping quality not in range ' \
                      '[0-(2^8-1)]'.format(intro)
            elif error.part == 5:
                msg = '{0} CIGAR string has characters not in ' \
                      '[0-9MIDNSHPX=]'.format(intro)
            elif error.part == 6:
                msg = '{0} mate read name has characters not in ' \
                      '[!-()+-<>-~][!-~]'.format(intro)
            elif error.part == 7:
                msg = '{0} mate read position not in range ' \
                      '[0-(2^31-1)]'.format(intro)
            elif error.part == 8:
                msg = '{0} template length not in range ' \
                      '[(-2^31+1)-(2^31-1)]'.format(intro)
            elif error.part == 9:
                msg = '{0} sequence has characters not in ' \
                      '[A-Za-z=.]'.format(intro)
            elif error.part == 10:
                msg = '{0} quality scores has characters not in ' \
                      '[!-~]'.format(intro)
            else:
                msg = '{0}: Unknown Error: Likely a Bug'.format(intro)
            raise FormatError(message=msg)

        if line:
            line += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('sam',
                        help='SAM file to verify [Default: STDIN]',
                        type=argparse.FileType('rU'),
                        default=sys.stdin)
    parser.add_argument('-q', '--quiet',
                        help='Suppresses message when file is good',
                        action='store_false')
    args = parser.parse_args()

    for entry in enumerate(sam_iter(args.sam, headers=True)):
        sam_verifier([entry[1]], line=entry[0] + 1)
    if not args.quiet:
        print('{0} is valid').format(args.sam.name)


if __name__ == '__main__':
    main()
    sys.exit(0)
