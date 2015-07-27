#!/usr/bin/env python

'''Verifies a FASTA file

Usage:

    fasta.py <fastaFile>
'''

__version__ = '1.1.0.0'

import argparse
from bio_utils.verifiers.line_verifier import verify_lines
from screed.fasta import fasta_iter
import sys

def fasta_verifier(handle, log_file = None):
    '''Returns True if FASTA file is valid and False if file is not valid'''

    lines = []
    for fastaEntry in fasta_iter(handle, parse_description = False):
        entry = '>{}\n{}\n'.format(fastaEntry['name'], fastaEntry['sequence'])
        lines.append(entry)
    regex = r'^>.+\n[ACGTURYKMSWBDHVNX]+\n$'
    delimiter = r'\n'
    fastaStatus = verify_lines(lines, regex, delimiter, log_file = log_file)
    return fastaStatus

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
                                     formatter_class = argparse.\
                                     RawDescriptionHelpFormatter)
    parser.add_argument('fastaFile',
                        help = 'FASTA file to verify')
    args = parser.parse_args()

    with open(args.fastaFile, 'rU') as in_handle:
        valid = fasta_verifier(in_handle)
    if valid:
        print('{} is valid'.format(args.fastaFile))
    else:
        print('{} is not valid'.format(args.fastaFile))
    sys.exit(0)
