#!/usr/bin/env python

'''Screed-esque iterator for FASTA files'''

__version__ = '1.0.4.0'

def fasta_iter(handle, parse_description=True):
    '''
    Iterator over the given FASTA file handle, returning records. handle
    is a handle to a file opened for reading.
    '''

    header = handle.next()

    for line in handle:

        if not header.startswith('>'):
            raise IOError("Bad FASTA format: no '>' at beginning of line")

        header = header.strip()
        data = {}
        if parse_description: # Try to grab the name and optional description
            try:
                data['name'], data['description'] = header[1:].split(' ', 1)
            except ValueError: # No optional description
                data['name'] = header[1:]
                data['description'] = ''
        else:
            data['name'] = header[1:]
            data['description'] = ''

        data['name'] = data['name'].strip()
        data['description'] = data['description'].strip()

        # Collect sequence lines into a list
        sequenceList = []
        while line and not line.startswith('>'):
            sequenceList.append(line.strip())
            line = handle.next()
        header = line

        data['sequence'] = ''.join(sequenceList)
        yield data
