#!/usr/bin/env python

'''Verifies a FASTA file'''

__version__ = '1.0.0.0'

from line_verifier import verify_lines
from screed.fasta import fasta_iter

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
