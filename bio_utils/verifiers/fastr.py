#!/usr/bin/env python

'''Verifies a FASTR file, compressed or decompressed

Usage:

    fastr <fastrFile>
'''

__version__ = '1.2.0.0'

import argparse
from bio_utils.verifiers.line_verifier import verify_lines
from bio_utils.iterators.fastr import fastr_iter
import sys

def fastr_verifier(handle, log_file = None):
    '''Returns True if FASTR file is valid and False if file is not valid'''

    lines = []
    for fastrEntry in fastr_iter(handle):
        entry = '+{}\n{}\n'.format(fastrEntry['name'], fastrEntry['sequence'])
        lines.append(entry)
    regex = r'^\+.+\n[\dx-]*\d\n$'
    delimiter = r'\n'
    fastrStatus = verify_lines(lines, regex, delimiter, log_file = log_file)
    return fastrStatus


def main():
    parser = argparse.ArgumentParser(description = __doc__,
                                     formatter_class = argparse.\
                                     RawDescriptionHelpFormatter)
    parser.add_argument('fastrFile',
                        help = 'FASTR file to verify')
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
