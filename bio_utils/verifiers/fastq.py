#!/usr/bin/env python

'''Verifies a FASTQ file'''

__version__ = '1.0.0.0'

from line_verifier import verify_lines
from screed.fastq import fastq_iter

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
