#!/usr/bin/env python

"""Screed-esque iterator for SAM files (not headers)"""

__version__ = '1.0.1.1'
__author__ = 'Alex Hyer'


def sam_iter(handle):
    """
    Iterator over the given SAM file handle, returning records. handle
    is a handle to a file opened for reading
    """

    for line in handle:

        if line.startswith('@'):
            continue

        line = line.strip()
        splitLine = line.split('\t')
        data = {
            'qname': splitLine[0],
            'flag': splitLine[1],
            'rname': splitLine[2],
            'pos': splitLine[3],
            'mapq': splitLine[4],
            'cigar': splitLine[5],
            'rnext': splitLine[6],
            'pnext': splitLine[7],
            'tlen': splitLine[8],
            'seq': splitLine[9],
            'qual': splitLine[10]
        }

        yield data
