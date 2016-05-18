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
__version__ = '3.0.0'


class FastqEntry:
    """A simple class to store data from FASTQ entries and write them

    Attributes:
            id (str): FASTQ ID (everything between the '@' and the first space
                of header line)
            description (str): FASTQ description (everything after the first
                space of the header line)
            sequence (str): FASTQ sequence
            quality (str): FASTQ quality csores
    """

    def __init__(self):
        """Initialize attributes to store FASTQ entry data"""

        self.id = None
        self.description = None
        self.sequence = None
        self.quality = None

    def write(self):
        """Return FASTQ formatted string

        Returns:
            str: FASTQ formatted string containing entire FASTQ entry
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

    Args:
        handle (file): FASTQ file handle, can be any iterator so long as it
            it returns subsequent "lines" of a FASTQ entry

        header (str): Header line of next FASTQ entry, if 'handle' has been
            partially read and you want to start iterating at the next entry,
            read the next FASTQ header and pass it to this variable when
            calling fastq_iter. See 'Examples.'

    Yields:
        FastqEntry: class containing all FASTQ data

    Raises:
        IOError: If FASTQ entry doesn't start with '@'

    Examples:
        The following two examples demonstrate how to use fastq_iter.
        Note: These doctests will not pass, examples are only in doctest
        format as per convention. bio_utils uses pytests for testing.

        >>> for entry in fastq_iter(open('test.fastq')):
        ...     print(entry.id)  # Print FASTQ id
        ...     print(entry.description)  # Print FASTQ description
        ...     print(entry.sequence)  # Print FASTQ sequence
        ...     print(entry.quality)  # Print FASTQ quality scores
        ...     print(entry.write())  # Print full FASTQ entry

        >>> fastq_handle = open('test.fastq')
        >>> next(fastq_handle)  # Skip first entry header
        >>> next(fastq_handle)  # Skip first entry sequence
        >>> next(fastq_handle)  # Skip line with '+'
        >>> next(fastq_handle)  # Skip first entry quality scores
        >>> first_line = next(fastq_handle)  # Read second entry header
        >>> for entry in fastq_iter(fastq_handle, header=first_line):
        ...     print(entry.id)  # Print FASTQ id
        ...     print(entry.description)  # Print FASTQ description
        ...     print(entry.sequence)  # Print FASTQ sequence
        ...     print(entry.quality)  # Print FASTQ quality scores
        ...     print(entry.write())  # Print full FASTQ entry
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
            while line and qual_len < seq_len:
                append(quality_list, line)
                qual_len += len(line)
                line = strip(next(handle))  # Raises StopIteration at EOF
            header = line  # Store current line so it's not lost next iteration
            data.quality = join('', quality_list)

            yield data

    except StopIteration:  # Yield last FASTQ entry
        data.quality = join('', quality_list)
        yield data
