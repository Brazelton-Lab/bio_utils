#!/usr/bin/env python

'''Verifies a GFF3 file

Usage:

    gff3.py <gff3File>
'''

__version__ = '1.1.0.0'

import argparse
from bio_utils.verifiers.line_verifier import verify_lines
from bio_utils.iterators.gff3 import gff3_iter
import sys

def gff3_verifier(handle, log_file = None):
    '''Returns True if GFF3 file is valid and False if file is not valid'''

    lines = []
    for gff3Entry in gff3_iter(handle):
        entry = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(\
                gff3Entry['seqid'], gff3Entry['source'], gff3Entry['type'],\
                gff3Entry['start'], gff3Entry['end'], gff3Entry['score'],\
                gff3Entry['strand'], gff3Entry['phase'],\
                gff3Entry['attributes'])
        lines.append(entry)
    regex = r'^[a-zA-Z0-9.:^*$@!+_?-|]+\t.+\t.+\t\d+\t\d+\t'\
            + r'\d*\.?\d*\t[+-.]\t[.0-2]\t.+\n$'
    delimiter = r'\t'
    gff3Status = verify_lines(lines, regex, delimiter, log_file = log_file)
    return gff3Status

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
                                     formatter_class = argparse.\
                                     RawDescriptionHelpFormatter)
    parser.add_argument('gff3File',
                        help = 'GFF3 file to verify')
    args = parser.parse_args()

    with open(args.gff3File, 'rU') as in_handle:
        valid = gff3_verifier(in_handle)
    if valid:
        print('{} is valid'.format(args.gff3File))
    else:
        print('{} is not valid'.format(args.gff3File))
    sys.exit(0)
