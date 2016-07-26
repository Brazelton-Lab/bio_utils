#! /usr/bin/env python

"""Screed-esque iterator for SAM files

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
__version__ = '3.0.1'


class SamEntry:
    """A simple class to store data from SAM entries and write them

    Attributes:
            qname (str): Name of query sequence

            flag (int): Int if integer in file, str if hex given in file,
                        str if flag not given. Gives various info about read
                        alignment, see
                        https://samtools.github.io/hts-specs/SAMv1.pdf
                        for more info.

            rname (str): Name of reference sequence or sequence aligned to

            pos (int): first base of alignment relative to reference,
                       0 = no alignment

            mapq (int): mapping quality of alignment

            cigar (str): CIGAR string detailing alignment

            rnext (str): name of paired read

            pnext (int): position of paired read, 0 = no alignment

            tlen (int): length of alignments of all paired reads

            seq (str): sequence of query sequence, * if no sequence

            qual (str): quality scores of query sequence, * if no scores
    """

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

        Returns:
            str: SAM formatted string containing entire SAM entry
        """

        return '{0}\t{1}\t{2}\t{3}\t{4}\t' \
               '{5}\t{6}\t{7}\t{8}\t{9}\t' \
               '{10}{11}'.format(self.qname,
                                 str(self.flag),
                                 self.rname,
                                 str(self.pos),
                                 str(self.mapq),
                                 self.cigar,
                                 self.rnext,
                                 str(self.pnext),
                                 str(self.tlen),
                                 self.seq,
                                 self.qual,
                                 os.linesep)


def sam_iter(handle, start_line=None, headers=False):
    """Iterate over SAM file and return SAM entries

    Args:
        handle (file): SAM file handle, can be any iterator so long as it
            it returns subsequent "lines" of a SAM entry

        start_line (str): Next SAM entry, if 'handle' has been partially read
            and you want to start iterating at the next entry, read the next
            SAM entry and pass it to this variable when calling sam_iter.
            See 'Examples.'

        headers (bool): Yields headers if True, else skips lines starting with
            "@"

    Yields:
        SamEntry: class containing all SAM data, yields str for headers if
            headers options is True then yields GamEntry for entries

    Examples:
        The following two examples demonstrate how to use sam_iter.
        Note: These doctests will not pass, examples are only in doctest
        format as per convention. bio_utils uses pytests for testing.

        >>> for entry in sam_iter(open('test.sam')):
        ...     print(entry.qname)  # Print query sequence name
        ...     print(entry.flag)  # Print flag number of alignment
        ...     print(entry.rname)  # Print reference sequence name
        ...     print(entry.pos)  # Print starting position of alignment
        ...     print(entry.mapq)  # Print mapping confidence of alignment
        ...     print(entry.cigar)  # Print CIGAR string of alignment
        ...     print(entry.rnext)  # Print paired read name
        ...     print(entry.pnext)  # Print position of paired read
        ...     print(entry.tlen)  # Print alignment length of all paired reads
        ...     print(entry.seq)  # Print query sequence
        ...     print(entry.qual)  # Print query quality scores
        ...     print(entry.write())  # Print whole SAM entry

        >>> sam_handle = open('test.gff3')
        >>> next(sam_handle)  # Skip first line/entry
        >>> next_line = next(sam_handle)  # Store next entry
        >>> for entry in sam_iter(open('test.sam')):
        ...     print(entry.qname)  # Print query sequence name
        ...     print(entry.flag)  # Print flag number of alignment
        ...     print(entry.rname)  # Print reference sequence name
        ...     print(entry.pos)  # Print starting position of alignment
        ...     print(entry.mapq)  # Print mapping confidence of alignment
        ...     print(entry.cigar)  # Print CIGAR string of alignment
        ...     print(entry.rnext)  # Print paired read name
        ...     print(entry.pnext)  # Print position of paired read
        ...     print(entry.tlen)  # Print alignment length of all paired reads
        ...     print(entry.seq)  # Print query sequence
        ...     print(entry.qual)  # Print query quality scores
        ...     print(entry.write())  # Print whole SAM entry
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

            if line.startswith('@') and not headers:
                line = strip(next(handle))
                continue
            elif line.startswith('@') and headers:
                yield line
                line = strip(next(handle))
                continue

            data = SamEntry()
            data.qname = split_line[0]
            try:  # Differentiate between int and hex bit flags
                data.flag = int(split_line[1])
            except ValueError:
                data.flag = split_line[1]
            data.rname = split_line[2]
            data.pos = int(split_line[3])
            data.mapq = int(split_line[4])
            data.cigar = split_line[5]
            data.rnext = split_line[6]
            data.pnext = int(split_line[7])
            data.tlen = int(split_line[8])
            data.seq = split_line[9]
            data.qual = split_line[10]

            line = strip(next(handle))  # Raises StopIteration at EOF

            yield data

    except StopIteration:  # Yield last SAM entry
        yield data
