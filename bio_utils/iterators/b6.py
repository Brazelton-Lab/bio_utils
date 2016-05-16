#!/usr/bin/env python

"""Screed-esque iterator for BLAST M8 (BLAST+ output format 6) files

Copyright:

    b6.py monitor iterate over and return entries of a B6/M8 file
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
__version__ = '3.0.1'


class B6Entry:
    """A simple class to store data from B6/M8 entries and write them"""

    def __init__(self):
        """Initialize variables to store B6/M8 entry data"""

        self.query = None
        self.subject = None
        self.perc_identical = None
        self.align_len = None
        self.mismatches = None
        self.gaps = None
        self.query_start = None
        self.query_end = None
        self.subject_start = None
        self.subject_end = None
        self.evalue = None
        self.bit_score = None

    def write(self):
        """Return B6/M8 formatted string

        :return: B6/M8 formatted string
        :rtype: str
        """

        return '{0}\t{1}\t{2}\t{3}\t{4}\t' \
               '{5}\t{6}\t{7}\t{8}\t{9}\t' \
               '{10}\t{11}{12}'.format(self.query,
                                       self.subject,
                                       str(self.perc_identical),
                                       str(self.align_len),
                                       str(self.mismatches),
                                       str(self.gaps),
                                       str(self.query_start),
                                       str(self.query_end),
                                       str(self.subject_start),
                                       str(self.subject_end),
                                       str(self.evalue),
                                       str(self.bit_score),
                                       os.linesep)


def b6_iter(handle, start_line=None):
    """Iterate over B6/M8 file and return B6/M8 entries

    :param handle: B6/M8 file handle, can technically be any iterator
    :type handle: File Object

    :param start_line: Header line of entry file handle is open to
    :type start_line: str
    """

    # Speed tricks: reduces function calls
    split = str.split
    strip = str.strip

    if start_line is None:
        line = strip(next(handle))  # Read first B6/M8 entry
    else:
        line = strip(start_line)  # Set header to given header

    # A manual 'for' loop isn't needed to read the file properly and quickly,
    # unlike fasta_iter and fastq_iter, but it is necessary begin iterating
    # partway through a file when the user gives a starting line.
    try:  # Manually construct a for loop to improve speed by using 'next'

        while True:  # Loop until StopIteration Exception raised

            split_line = split(line, '\t')

            data = B6Entry()
            data.query = split_line[0]
            data.subject = split_line[1]
            data.perc_identical = float(split_line[2])
            data.align_len = int(split_line[3])
            data.mismatches = int(split_line[4])
            data.gaps = int(split_line[5])
            data.query_start = int(split_line[6])
            data.query_end = int(split_line[7])
            data.subject_start = int(split_line[8])
            data.subject_end = int(split_line[9])
            data.evalue = float(split_line[10])
            data.bit_score = int(split_line[11])

            line = strip(next(handle))  # Raises StopIteration at EOF

            yield data

    except StopIteration:  # Yield last B6/M8 entry
        yield data
