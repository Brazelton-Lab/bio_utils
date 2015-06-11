#!/usr/bin/env python

'''Screed-esque iterator for GFF3 files (not headers)'''

__version__ = '1.0.0.0'

def gff3_iter(handle):
    '''
    Iterator over the given GFF3 file handle, returning records. handle
    is a handle to a file opened for reading
    '''
        
    for line in handle:
        
        if line.startswith('##'):
            continue

        if line.startswith('>'):
            break

        line = line.strip()
        data = {}
        splitLine = line.split('\t')
        data['seqid'] = splitLine[0]
        data['source'] = splitLine[1]
        data['type'] = splitLine[2]
        data['start'] = splitLine[3]
        data['end'] = splitLine[4]
        data['score'] = splitLine[5]
        data['strand'] = splitLine[6]
        data['phase'] = splitLine[7]
        data['attributes'] = splitLine[8]
        
        yield data
