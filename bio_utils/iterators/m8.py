#!/usr/bin/env python

"""Screed-esque iterator for BLAST M8 (BLAST+ output format 6) files"""

__version__ = '1.0.1.0'
__author__ = 'Alex Hyer'


def m8_iter(handle):
    """
    Iterator over the given M8 file handle, returning records. handle
    is a handle to a file opened for reading
    """

    for line in handle:
        line = line.strip()
        split_line = line.split('\t')
        data = {
            'queryID': split_line[0],
            'subjectID': split_line[1],
            'percIdentical': split_line[2],
            'alignLen': split_line[3],
            'mismatchCount': split_line[4],
            'gapCount': split_line[5],
            'queryStart': split_line[6],
            'queryEnd': split_line[7],
            'subjectStart': split_line[8],
            'subjectEnd': split_line[9],
            'eValue': split_line[10],
            'bitScore': split_line[11]
            }

        yield data
