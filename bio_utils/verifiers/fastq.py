#!/usr/bin/env python

from __future__ import print_function

"""Verifies a FASTQ file

Usage:

    fastq_verifier <fastqFile>
"""

__version__ = '1.2.0.1'
__author__ = 'Alex Hyer'

import argparse
from bio_utils.verifiers.line_verifier import verify_lines
from screed.fastq import fastq_iter
import sys


def fastq_verifier(handle):
    """Returns True if FASTQ file is valid and False if file is not valid"""

    lines = []
    for fastq_entry in fastq_iter(handle):
        entry = '@{}\n{}\n+\n{}\n'.format(fastq_entry['name'],
                                          fastq_entry['sequence'],
                                          fastq_entry['quality'])
        lines.append(entry)
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
