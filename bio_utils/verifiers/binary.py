#!/usr/bin/env python

from __future__ import print_function

"""Guesses if a file is binary or not

Usage:

    binary_verifier <binaryFile>
"""

__version__ = '1.2.1.0'
__author__ = 'Alex Hyer'
__credits__ = 'Andrew Dalke'

import argparse
import string
import sys


# Credit: http://code.activestate.com/
# recipes/173220-test-if-a-file-or-string-is-text-or-binary/

def binary_verifier(handle):
    """Returns True if file is probably binary and False if not"""

    text_characters = ''.join(map(chr, range(32, 127)) + list('\n\r\t\b'))
    null_trans_table = string.maketrans('', '')
    first_block = handle.read(512)
    filtered_block = first_block.translate(null_trans_table, text_characters)
    if float(len(filtered_block)) / float(len(first_block)) > 0.30:
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('binaryFile',
                        help='file to verify if binary')
    args = parser.parse_args()

    with open(args.binaryFile, 'rU') as in_handle:
        valid = binary_verifier(in_handle)
    if valid:
        print('{} is probably a binary file'.format(args.binaryFile))
    else:
        print('{} is probably a binary file'.format(args.binaryFile))


if __name__ == '__main__':
    main()
    sys.exit(0)
