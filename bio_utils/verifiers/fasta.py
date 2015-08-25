#!/usr/bin/env python

from __future__ import print_function

"""Verifies a FASTA file

Usage:

    fasta_verifier <fastaFile>
"""

__version__ = '1.3.0.1'
__author__ = 'Alex Hyer'

import argparse
from bio_utils.verifiers.line_verifier import verify_lines
from bio_utils.iterators.fasta import fasta_iter
import sys


def fasta_verifier(handle):
    """Returns True if FASTA file is valid and False if file is not valid"""

    lines = []
    for fastaEntry in fasta_iter(handle, parse_description=False):
        entry = '>{}\n{}\n'.format(fastaEntry['name'], fastaEntry['sequence'])
        lines.append(entry)
    regex = r'^>.+\n[ACGTURYKMSWBDHVNX]+\n$'
    delimiter = r'\n'
    fasta_status = verify_lines(lines, regex, delimiter)
    return fasta_status


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('fastaFile',
                        help='FASTA file to verify')
    args = parser.parse_args()

    with open(args.fastaFile, 'rU') as in_handle:
        valid = fasta_verifier(in_handle)
    if valid:
        print('{} is valid'.format(args.fastaFile))
    else:
        print('{} is not valid'.format(args.fastaFile))


if __name__ == '__main__':
    main()
    sys.exit(0)
