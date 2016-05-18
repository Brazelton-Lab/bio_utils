#! /usr/bin/env python

"""Faster, simpler, Screed-esque iterator for FASTA files

Copyright:

    fasta.py iterate over and return entries of a FASTA file
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


class FastaEntry:
    """A simple class to store data from FASTA entries and write them

    Attributes:
            id (str): FASTA ID (everything between the '>' and the first space
                of header line)
            description (str): FASTA description (everything after the first
                space of the header line)
            sequence (str): FASTA sequence
    """

    def __init__(self):
        """Initialize attributes to store FASTA entry data"""

        self.id = None
        self.description = None
        self.sequence = None

    def write(self):
        """Return FASTA formatted string

        Returns:
            str: FASTA formatted string containing entire FASTA entry
        """

        if self.description:
            return '>{0} {1}{3}{2}{3}'.format(self.id,
                                              self.description,
                                              self.sequence,
                                              os.linesep)
        else:
            return '>{0}{2}{1}{2}'.format(self.id,
                                          self.sequence,
                                          os.linesep)


def fasta_iter(handle, header=None):
    """Iterate over FASTA file and return FASTA entries

    Args:
        handle (file): FASTA file handle, can be any iterator so long as it
            it returns subsequent "lines" of a FASTA entry

        header (str): Header line of next FASTA entry, if 'handle' has been
            partially read and you want to start iterating at the next entry,
            read the next FASTA header and pass it to this variable when
            calling fasta_iter. See 'Examples.'

    Yields:
        FastaEntry: class containing all FASTA data

    Raises:
        IOError: If FASTA entry doesn't start with '>'

    Examples:
        The following two examples demonstrate how to use fasta_iter.
        Note: These doctests will not pass, examples are only in doctest
        format as per convention. bio_utils uses pytests for testing.

        >>> for entry in fasta_iter(open('test.fasta')):
        ...     print(entry.id)  # Print FASTA id
        ...     print(entry.description)  # Print FASTA description
        ...     print(entry.sequence)  # Print FASTA sequence
        ...     print(entry.write())  # Print full FASTA entry

        >>> fasta_handle = open('test.fasta')
        >>> next(fasta_handle)  # Skip first entry header
        >>> next(fasta_handle)  # Skip first entry sequence
        >>> first_line = next(fasta_handle)  # Read second entry header
        >>> for entry in fasta_iter(fasta_handle, header=first_line):
        ...     print(entry.id)  # Print FASTA id
        ...     print(entry.description)  # Print FASTA description
        ...     print(entry.sequence)  # Print FASTA sequence
        ...     print(entry.write())  # Print full FASTA entry
    """

    # Speed tricks: reduces function calls
    append = list.append
    join = str.join
    strip = str.strip

    if header is None:
        header = strip(next(handle))  # Read first FASTA entry header
    else:
        header = strip(header)  # Set header to given header

    try:  # Manually construct a for loop to improve speed by using 'next'

        while True:  # Loop until StopIteration Exception raised

            line = strip(next(handle))

            data = FastaEntry()

            if not header[0] == '>':
                raise IOError('Bad FASTA format: no ">" at beginning of line')

            try:
                data.id, data.description = header[1:].split(' ', 1)
            except ValueError:  # No description
                data.id = header[1:]
                data.description = ''

            # Obtain sequence
            sequence_list = []
            while line and not line[0] == '>':
                append(sequence_list, line)
                line = strip(next(handle))  # Raises StopIteration at EOF
            header = line  # Store current line so it's not lost next iteration
            data.sequence = join('', sequence_list)

            yield data

    except StopIteration:  # Yield last FASTA entry
        data.sequence = ''.join(sequence_list)
        yield data
