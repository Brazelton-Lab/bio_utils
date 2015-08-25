#!/usr/bin/env python

from __future__ import print_function

"""Verifies a FASTR file, compressed or decompressed

Usage:

    fastr_verifier <fastrFile>
"""

__version__ = '1.3.0.1'
__author__ = 'Alex Hyer'

import argparse
from bio_utils.verifiers.line_verifier import verify_lines
from bio_utils.iterators.fastr import fastr_iter
import sys


def fastr_verifier(handle):
    """Returns True if FASTR file is valid and False if file is not valid"""

    lines = []
    for fastrEntry in fastr_iter(handle):
        entry = '+{}\n{}\n'.format(fastrEntry['name'], fastrEntry['sequence'])
        lines.append(entry)
    regex = r'^\+.+\n[\dx-]*\d\n$'
    delimiter = r'\n'
    fastr_status = verify_lines(lines, regex, delimiter)
    return fastr_status


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('fastrFile',
                        help='FASTR file to verify')
    args = parser.parse_args()

    with open(args.fastrFile, 'rU') as in_handle:
        valid = fastr_verifier(in_handle)
    if valid:
        print('{} is valid'.format(args.fastrFile))
    else:
        print('{} is not valid'.format(args.fastrFile))


if __name__ == '__main__':
    main()
    sys.exit(0)
