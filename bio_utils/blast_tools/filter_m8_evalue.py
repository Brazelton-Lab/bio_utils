#! /usr/bin/env python

"""Writes lines from the M8 file under the given e-value to output

Usage:

    m8_evalue_filter.py --m8_file [m8_file] --e_value [e_value]
                        --output [output]
"""

from __future__ import print_function
import argparse
from bio_utils.iterators import m8_iter
import sys

__author__ = 'William Brazelton, Alex Hyer'
__version__ = '1.1.2'


def m8_evalue_filter(handle, e_value):
    """Returns lines from handle with e-value less than or equal to e_value

    :returns: yields M8 entries below e-value cutoff
    :rtype: dict

    :param handle: file handle of M8 file
    :type handle: file object

    :param e_value: upper e-value threshold
    :type e_value: float
    """

    for entry in m8_iter(handle):
        if float(entry['eValue']) <= e_value:
            yield entry


def main():
    with open(args.m8_file, 'rU') as m8_handle:
        for entry in m8_evalue_filter(m8_handle, args.e_value):
            entry = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n' \
                .format(entry['queryID'], entry['subjectID'],
                        entry['percIdentical'], entry['alignLen'],
                        entry['mismatchCount'], entry['gapCount'],
                        entry['queryStart'], entry['queryEnd'],
                        entry['subjectStart'], entry['subjectEnd'],
                        entry['eValue'], entry['bitScore'])
            args.output.write(entry)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('-m', '--m8_file',
                        nargs='?',
                        type=argparse.FileType('rU'),
                        default=sys.stdin,
                        help='M8 (B6 in BLAST+) file with alignment data'
                             '[Default: STDIN]')
    parser.add_argument('-e', '--e_value',
                        type=float,
                        help='upper e-value cutoff')
    parser.add_argument('-o', '--output',
                        nargs='?',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='optional output file [Default: STDOUT]')
    args = parser.parse_args()

    main()
    sys.exit(0)
