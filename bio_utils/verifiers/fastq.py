#!/usr/bin/env python

'''Verifies a FASTQ file

Usage:

    fastq.py <fastqFile>
'''

__version__ = '1.0.0.0'

import argparse
from bio_utils.verifiers.line_verifier import verify_lines
from screed.fastq import fastq_iter
import sys

def fastq_verifier(handle, log_file = None):
    '''Returns True if FASTQ file is valid and False if file is not valid'''

    lines = []
    for fastqEntry in fastq_iter(handle):
        entry = '@{}\n{}\n+\n{}\n'.format(fastqEntry['name'],
                                          fastqEntry['sequence'],
                                          fastqEntry['quality'])
        lines.append(entry)
    regex = r'^@.+\n[ACGTURYKMSWBDHVNX]+\n\+.*\n.+\n$'
    delimiter = r'\n'
    fastqStatus = verify_lines(lines, regex, delimiter, log_file = log_file)
    return fastqStatus

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
                                     formatter_class = argparse.\
                                     RawDescriptionHelpFormatter)
    parser.add_argument('fastqFile',
                        help = 'FASTQ file to verify')
    args = parser.parse_args()

    with open(args.fastqFile, 'rU') as in_handle:
        valid = fastq_verifier(in_handle)
    if valid:
        print('{} is valid'.format(args.fastqFile))
    else:
        print('{} is not valid'.format(args.fastqFile))
    sys.exit(0)
