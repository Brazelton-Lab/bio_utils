#!/usr/bin/env python

"""Screed-esque iterator for GFF3 files (not headers)"""

__version__ = '1.2.3.1'
__author__ = 'Alex Hyer'


def gff3_iter(handle, prokka=False):
    """
    Iterator over the given GFF3 file handle, returning records. handle
    is a handle to a file opened for reading. The PROKKA option
    further parses the attributes by the GFF3 output of PROKKA 1.12-beta
    """

    for line in handle:

        if line == '##FASTA\n':
            break

        if line.startswith('##'):
            continue

        line = line.strip()
        split_line = line.split('\t')
        data = {
            'seqid': split_line[0],
            'source': split_line[1],
            'type': split_line[2],
            'start': split_line[3],
            'end': split_line[4],
            'score': split_line[5],
            'strand': split_line[6],
            'phase': split_line[7],
            'attributes': split_line[8]
            }

        if prokka:
            attributes = data['attributes'].split(';')
            for attribute in attributes:
                split_attribute = attribute.split('=')
                key = split_attribute[0]
                value = split_attribute[-1]
                data[key] = value

        yield data
