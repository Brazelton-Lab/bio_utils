#! /usr/bin/env python

"""Faster, simpler, Screed-esque iterator for FASTQ files

Copyright:

    fastq.py iterate over and return entries of a FASTQ file
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
__version__ = '2.1.1'


class FastqEntry:
    """A simple class to store data from FASTQ entries and write them"""

    def __init__(self):
        """Initialize variables to store FASTQ entry data"""

        self.id = None
        self.description = None
        self.sequence = None
        self.quality = None

    def write(self):
        """Return FASTQ formatted string

        :return: FASTQ formatted string
        :rtype: str
        """

        if self.description:
            return '@{0} {1}{4}{2}{4}+{4}{3}{4}'.format(self.id,
                                                        self.description,
                                                        self.sequence,
                                                        self.quality,
                                                        os.linesep)
        else:
            return '@{0}{3}{1}{3}+{3}{2}{3}'.format(self.id,
                                                    self.sequence,
                                                    self.quality,
                                                    os.linesep)


def fastq_iter(handle, header=None):
    """Iterate over FASTQ file and return FASTQ entries

    :param handle: FASTQ file handle, can technically be any iterator
    :type handle: File Object

    :param header: Header line of entry file handle is open to
    :type header: str

    :return: class containing FASTQ data
    :rtype: FastqEntry
    """

    # Speed tricks: reduces function calls
    append = list.append
    join = str.join
    strip = str.strip

    if header is None:
        header = strip(next(handle))  # Read first FASTQ entry header
    else:
        header = strip(header)  # Set header to given header

    try:  # Manually construct a for loop to improve speed by using 'next'

        while True:  # Loop until StopIteration Exception raised

            line = strip(next(handle))

            data = FastqEntry()

            if not header[0] == '@':
                raise IOError('Bad FASTQ format: no "@" at beginning of line')

            try:
                data.id, data.description = header[1:].split(' ', 1)
            except ValueError:  # No description
                data.id = header[1:]
                data.description = ''

            # obtain sequence
            sequence_list = []
            while line and not line[0] == '+' and not line[0] == '#':
                append(sequence_list, line)
                line = strip(next(handle))
            data.sequence = join('', sequence_list)

            line = strip(next(handle))  # Skip line containing only '+'

            # Obtain quality scores
            quality_list = []
            seq_len = len(data.sequence)
            qual_len = 0
            while line and not line[0] == '@' and qual_len < seq_len:
                append(quality_list, line)
                qual_len += len(line)
                line = strip(next(handle))  # Raises StopIteration at EOF
            header = line  # Store current line so it's not lost next iteration
            data.quality = join('', quality_list)

            yield data

    except StopIteration:  # Yield last FASTQ entry
        data.quality = join('', quality_list)
        yield data
