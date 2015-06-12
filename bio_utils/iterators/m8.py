#!/usr/bin/env python

'''Screed-esque iterator for BLAST M8 files'''

__version__ = '1.0.0.0'

def m8_iter(handle):
    '''
    Iterator over the given M8 file handle, returning records. handle
    is a handle to a file opened for reading
    '''

    for line in handle:

        line = line.strip()
        splitLine = line.split('\t')
        data = {}
        data['queryID'] = splitLine[0]
        data['subjectID'] = splitLine[1]
        data['percIdentical'] = splitLine[2]
        data['alignLen'] = splitLine[3]
        data['mismatchCount'] = splitLine[4]
        data['gapCount'] = splitLine[5]
        data['queryStart'] = splitLine[6]
        data['queryEnd'] = splitLine[7]
        data['subjectStart'] = splitLine[8]
        data['subjectEnd'] = splitLine[9]
        data['eValue'] = splitLine[10]
        data['bitScore'] = splitLine[11]

        yield data
