#!/usr/bin/env python

'''Verifies a GFF3 file'''

__version__ = '1.0.0.0'

from line_verifier import verify_lines
from bio_utils.iterators.gff3 import gff3_iter

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
