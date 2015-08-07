#!/usr/bin/env python

'''Screed-esque iterator for FASTA files'''

__version__ = '1.0.0.0'

def fasta_iter(handle, parse_description=True):
    '''
    Iterator over the given FASTA file handle, returning records. handle
    is a handle to a file opened for reading.
    '''

    for line in handle:

        if not line.startswith('>'):
            raise IOError("Bad FASTA format: no '>' at beginning of line")

        line = line.strip()
        data ={}
        if parse_description: # Try to grab the name and optional description
            try:
                data['name'], data['description'] = line[1:].split(' ', 1)
            except ValueError: # No optional description
                data['name'] = line[1:]
                data['description'] = ''
        else:
            data['name'] = line[1:]
            data['description'] = ''

        data['name'] = data['name'].strip()
        data['description'] = data['description'].strip()

        yield data