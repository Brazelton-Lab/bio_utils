#!/usr/bin/env python

"""Verifies a SAM file


Usage:

    sam_verifier <samFile>
"""

__version__ = '1.1.1.0'
__author__ = 'Alex Hyer'

import argparse
from bio_utils.verifiers.line_verifier import verify_lines
from bio_utils.iterators.sam import sam_iter
import sys


def sam_verifier(handle):
    """Returns True if SAM file is valid and False if file is not valid"""

    lines = []
    for samEntry in sam_iter(handle):
        entry = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t%s{}\t{}\n'.format(
            samEntry['qname'],
            samEntry['flag'],
            samEntry['rname'],
            samEntry['pos'],
            samEntry['mapq'],
            samEntry['cigar'],
            samEntry['rnext'],
            samEntry['pnext'],
            samEntry['tlen'],
            samEntry['seq'],
            samEntry['qual'])
        lines.append(entry)
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
            + r'[!-~]+\n$'
    delimiter = r'\t'
    sam_status = verify_lines(lines, regex, delimiter)
    return sam_status


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse. \
                                     RawDescriptionHelpFormatter)
    parser.add_argument('samFile',
                        help='SAM file to verify')
    args = parser.parse_args()

    with open(args.samFile, 'rU') as in_handle:
        valid = sam_verifier(in_handle)
    if valid:
        print('{} is valid'.format(args.samFile))
    else:
        print('{} is not valid'.format(args.samFile))


if __name__ == '__main__':
    main()
    sys.exit(0)
