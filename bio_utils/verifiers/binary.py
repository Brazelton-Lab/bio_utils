#!/usr/bin/env python

'''Guesses if a file is binary or not'''

__version__ = '1.0.0.0'

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
