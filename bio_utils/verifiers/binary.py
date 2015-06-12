#!/usr/bin/env python

'''Guesses if a file is binary or not

Usage:

    binary.py <binaryFile>
'''

__version__ = '1.1.0.0'

import argparse
import string
import sys

# Credit: http://code.activestate.com/
# recipes/173220-test-if-a-file-or-string-is-text-or-binary/

def binary_verifier(handle):
    '''Returns True if file is probably binary and False if not'''

    textCharacters = ''.join(map(chr, range(32, 127)) + list('\n\r\t\b'))
    nullTransTable = string.maketrans('', '')
    firstBlock = handle.read(512)
    filteredBlock = firstBlock.translate(nullTransTable, textCharacters)
    if float(len(filteredsBlock))/float(len(firstBlock)) > 0.30:
        return True
    else:
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
                                     formatter_class = argparse.\
                                     RawDescriptionHelpFormatter)
    parser.add_argument('binaryFile',
                        help = 'file to verify if binary')
    args = parser.parse_args()

    with open(args.binaryFile, 'rU') as in_handle:
        valid = binary_verifier(in_handle)
    if valid:
        print('{} is probably a binary file'.format(args.binaryFile))
    else:
        print('{} is probably a binary file'.format(args.binaryFile))
    sys.exit(0)
