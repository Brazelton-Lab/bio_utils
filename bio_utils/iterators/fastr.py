#!/usr/bin/env python

'''Screed-esque iterator for FASTR files'''

__version__ = '1.0.0.0'

from metameta.metameta_utils.compress_fastr import compress_fastr
from metameta.metameta_utils.decompress_fastr import decompress_fastr

def fastr_iter(handle, parse_description = True, line = None,\
               compressed = None):
    '''
    Iterator over the given FASTR file handle, returning records. handle
    is a handle to a file opened for reading
    '''

    if line == None:
        line = handle.readline()
        
    while line:
        
        if not line.startswith('+'):
            raise IOError("Bad FASTR format: no '+' at beginning of line")

        data = {}
        line = line.strip()
        
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

        # Collect sequence lines into a list
        sequenceList = []
        line = handle.readline()
        while line and not line.startswith('+'):
            sequenceList.append(line.strip())
            line = handle.readline()

        sequenceString = ''.join(sequenceList)
        if compressed == 'compressed':
            data['sequence'] = compress_fastr(sequenceString)
        elif compressed == 'decompressed':
            data['sequence'] = decompress_fastr(sequenceString)
        else:
            data['sequence'] = sequenceString
        yield data
