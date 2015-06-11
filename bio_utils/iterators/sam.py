#!/usr/bin/env python

'''Screed-esque iterator for SAM files (not headers)'''

__version__ = '1.0.0.0'

def sam_iter(handle):
    '''
    Iterator over the given SAM file handle, returning records. handle
    is a handle to a file opened for reading
    '''

    for line in handle:
        
        if line.startswith('@'):
            continue

        line = line.strip()
        data = {}
        splitLine = line.split('\t')
        data['qname'] = splitLine[0]
        data['flag'] = splitLine[1]
        data['rname'] = splitLine[2]
        data['pos'] = splitLine[3]
        data['mapq'] = splitLine[4]
        data['cigar'] = splitLine[5]
        data['rnext'] = splitLine[6]
        data['pnext'] = splitLine[7]
        data['tlen'] = splitLine[8]
        data['seq'] = splitLine[9]
        data['qual'] = splitLine[10]
        
        yield data
