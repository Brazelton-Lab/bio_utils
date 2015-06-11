#!/usr/bin/env python

'''Verifies a FASTR file, compressed or decompressed'''

__version__ = '1.0.0.0'

from line_verifier import verify_lines
from bio_utils.iterators.fastr import fastr_iter

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
