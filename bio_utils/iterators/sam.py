#!/usr/bin/env python

"""Screed-esque iterator for SAM files (not headers)

Copyright:

    sam.py iterate over and return entries of a SAM file
    Copyright (C) 2015  William Brazelton, Alex Hyer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '2.0.0'


class SamEntry:
    """A simple class to store data from SAM entries and write them"""

    def __init__(self):
        """Initialize variables to store SAM entry data"""

        self.qname = None
        self.flag = None
        self.rname = None
        self.pos = None
        self.mapq = None
        self.cigar = None
        self.rnext = None
        self.pnext = None
        self.tlen = None
        self.seq = None
        self.qual = None

    def write(self):
        """Return SAM formatted string

        :return: SAM formatted string
        :rtype: str
        """

        return '{0}\t{1}\t{2}\t{3}\t{4}\t' \
               '{5}\t{6}\t{7}\t{8}\t{9}\t' \
               '{10}{11}'.format(self.qname,
                                 self.flag,
                                 self.rname,
                                 self.pos,
                                 self.mapq,
                                 self.cigar,
                                 self.rnext,
                                 self.pnext,
                                 self.tlen,
                                 self.seq,
                                 self.qual,
                                 os.linesep)


def sam_iter(handle, start_line=None):
    """Iterate over SAM file and return B6/M8 entries

    :param handle: SAM file handle
    :type handle: File Object

    :param start_line: Header line of entry file handle is open to
    :type start_line: str
    """

    # Speed tricks: reduces function calls
    split = str.split
    strip = str.strip

    if start_line is None:
        line = strip(handle.next())  # Read first B6/M8 entry
    else:
        line = strip(start_line)  # Set header to given header

    # A manual 'for' loop isn't needed to read the file properly and quickly
    # unlike fasta_iter and fastq_iter, but it is necessary begin iterating
    # partway through a file when the user gives a starting line.
    try:  # Manually construct a for loop to improve speed by using 'next'

        while True:  # Loop until StopIteration Exception raised

            split_line = line.split('\t')

            if line.startswith('@'):
                line = strip(handle.next())
                continue

            data = SamEntry()
            data.qname = split_line[0]
            data.flag = split_line[1]
            data.rname = split_line[2]
            data.pos = split_line[3]
            data.mapq = split_line[4]
            data.cigar = split_line[5]
            data.rnext = split_line[6]
            data.pnext = split_line[7]
            data.tlen = split_line[8]
            data.seq = split_line[9]
            data.qual = split_line[10]

            line = strip(handle.next())  # Raises StopIteration at EOF

            yield data

    except StopIteration:
        pass
    finally:  # Yield last SAM entry
        yield data
