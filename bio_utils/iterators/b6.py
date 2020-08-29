#! /usr/bin/env python3

"""Iterator for BLAST M8 (BLAST+ output format 6) files

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

from collections import OrderedDict
import os
import sys

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '5.0.1'


class FormatError(Exception):
    """A simple exception that is raised when an input file is formatted 
    incorrectly
    """
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


class B6Entry:
    """A simple class to store data from B6/M8 entries and write them

    Attributes:
        fs_order (dict): dictionary storing the original order of the format
            specifiers with names as keys and indices as values

        query (str): query ID (sequence aligned with)

        subject (str): subject ID (sequence aligned to)

        identity (float): percentage of aligned bases between the subject 
            and query that are identical

        length (int): length of alignment (number of aligned bases)

        mismatches (int): number of mismatches in the alignment

        gaps (int): number of gaps in the alignment

        query_start (int): alignment start position in query sequence

        query_end (int): alignment end position in query sequence

        subject_start (int): alignment start position in subject sequence

        subject_end (int): alignment end position in subject sequence

        evalue (float): E-value of alignment

        bitscore (float): Bit score of alignment

        custom_fs (dict): OrderedDict of non-default format specifiers
    """

    def __init__(self):
        """Initialize variables to store B6/M8 entry data"""

        self.fs_order = None
        self.query = None
        self.subject = None
        self.identity = None
        self.length = None
        self.mismatches = None
        self.gaps = None
        self.query_start = None
        self.query_end = None
        self.subject_start = None
        self.subject_end = None
        self.evalue = None
        self.bitscore = None
        self.custom_fs = None  # Store additional format specifiers

    def write(self, default: bool=False):
        """Restore B6/M8 entry to original format

        Args:
            default (bool): output entry in default BLAST+ B6 format 

        Returns:
            str: properly formatted string containing the B6/M8 entry
        """

        none_type = type(None)

        if default:  # Default order of format specifiers
            ordered_vals = [getattr(self, i) for i in ['query', 'subject', 
                            'identity', 'length', 'mismatches', 'gaps', 
                            'query_start', 'query_end', 'subject_start', 
                            'subject_end', 'evalue', 'bitscore']]
        else:  # Original order of B6 entry format specifiers
            try:
                ordered_vals = [self.custom_fs[i] if i in self.custom_fs 
                            else getattr(self, i) for i in self.fs_order]
            except TypeError:
                ordered_vals = [getattr(self, i) for i in self.fs_order]

        # Format entry for writing
        fstr = "\t".join(['-' if type(i) == none_type else str(i) for i in 
                        ordered_vals])

        return '{}{}'.format(fstr, os.linesep)


class B6Reader():
    """Class to read from B6/M8 files and store lines as B6Entry objects

    Attributes:
        handle (file): B6/M8 file handle, can be any iterator so long as it
            it returns subsequent "lines" of a B6/M8 entry

        filename (str): name of the B6 file
    
        current_line (int): current line in file [default: 0]
    """

    def __init__(self, handle):
        """Initialize variables to store B6/M8 file information"""

        self.handle = handle
        self.filename = handle.name
        self.current_line = 0

    def iterate(self, start_line=None, header: list=['qaccver', 'saccver', 
        'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart',
        'send', 'evalue', 'bitscore'], comments: bool=False):
        """Iterate over B6/M8 file and return B6/M8 entries

        Args:
            start_line (str): Next B6/M8 entry. If 'handle' has been partially
                read and you want to start iterating at the next entry, read 
                the next B6/M8 entry and pass it to this variable when calling 
                b6_iter. See 'Examples' for proper usage.

            header (list): List of custom format specifiers if B6 file not in 
                default Blast+ 6 format

            comments (bool): Yields comments if True, else skips lines starting
                with "#"

        Yields:
            B6Entry: class containing all B6/M8 data

        Examples:
            The following two examples demonstrate how to use b6_iter.
            Note: These doctests will not pass, examples are only in doctest
            format as per convention. bio_utils uses pytests for testing.

            >>> for entry in b6_iter(open('test.b6out')):
            ...     print(entry.query)  # Query ID
            ...     print(entry.subject)  # Subject ID
            ...     print(entry.identity)  # Percent identity between seqs
            ...     print(entry.mismatches)  # Number mismatches in alignment
            ...     print(entry.gaps)  # Number gaps in alignment
            ...     print(entry.query_start)  # Start of alignment on query
            ...     print(entry.query_end)  # End of alignment on query
            ...     print(entry.subject_start)  # Start of align on subject
            ...     print(entry.subject_end)  # End of alignment on subject
            ...     print(entry.evalue)  # E-value of alignment
            ...     print(entry.bitscore)  # Bitscore of alignment
            ...     print(entry.write())  # Reconsitituted B6 entry

            >>> b6_handle = open('test.b6out')
            >>> next(b6_handle)  # Skip first line/entry
            >>> next_line = next(b6_handle)  # Store next entry
            >>> for entry in b6_iter(b6_handle, start_line=next_line):
            ...     print(entry.query)  # Query ID
            ...     print(entry.subject)  # Subject ID
            ...     print(entry.identity)  # Percent identity between seqs
            ...     print(entry.mismatches)  # Number mismatches in alignment
            ...     print(entry.gaps)  # Number gaps in alignment
            ...     print(entry.query_start)  # Start of alignment on query
            ...     print(entry.query_end)  # End of alignment on query
            ...     print(entry.subject_start)  # Start of align on subject
            ...     print(entry.subject_end)  # End of alignment on subject
            ...     print(entry.evalue)  # E-value of alignment
            ...     print(entry.bitscore)  # Bitscore of alignment
            ...     print(entry.write())  # Reconstituted B6 entry
        """

        handle = self.handle

        # Speed tricks: reduces function calls
        split = str.split
        strip = str.strip

        # Map attribute names to default format specifier names
        def_map = {'query_end': ('qend', str), 
                   'mismatches': ('mismatch', int), 
                   'identity': ('pident', float), 
                   'query': ('qaccver', str),
                   'query_start': ('qstart', int), 
                   'subject_start': ('sstart', int), 
                   'bitscore': ('bitscore', float), 
                   'evalue': ('evalue', float), 
                   'gaps': ('gapopen', int), 
                   'subject_end': ('send', int),
                   'length': ('length', int), 
                   'subject': ('saccver', str)
                  }

        def_map_rev = {j[0]: k for k, j in def_map.items()}
        def_specs = list(def_map_rev.keys())

        uheader = list(OrderedDict.fromkeys(header))
        spec_order = [def_map_rev[i] if i in def_map_rev else i \
                      for i in uheader]

        # Store order of format specifiers
        h = {}
        for index, specifier in enumerate(header):
            if specifier not in h:  # Ignor duplicate columns
                h[specifier] = index

        # Begin reading text
        if start_line is None:
            line = next(handle)  # Read first B6/M8 entry
        else:
            line = start_line  # Set header to given header

        # Check if input is text or bytestream
        if (isinstance(line, bytes)):
            def next_line(i):
                return next(i).decode('utf-8')

            line = strip(line.decode('utf-8'))
        else:
            next_line = next
            line = strip(line)

        # Manual 'for' loop isn't needed to read the file properly and quickly,
        # unlike fasta_iter and fastq_iter, but it is necessary begin iterating
        # partway through a file when the user gives a starting line.
        try:  # Manually construct a for loop to improve speed by using 'next'

            while True:  # Loop until StopIteration Exception raised

                self.current_line += 1

                data = B6Entry()
                data.fs_order = spec_order  # All entries store original order

                if line.startswith('#') and not comments:
                    line = strip(next_line(handle))
                    continue
                elif line.startswith('#') and comments:
                    yield line
                    line = strip(next_line(handle))
                    continue

                split_line = split(line, '\t')

                # Replace empty values with None
                spec_values = [None if i == '-' else i for i in split_line]

                # Add default specifiers
                def_attrs = data.__dict__.keys()
                for attr in def_attrs:
                    try:
                        def_spec, spec_type = def_map[attr]
                    except KeyError:
                        continue

                    try:
                        value = spec_values[h[def_spec]]
                    except KeyError:  # Custom format, no value
                        continue
                    except IndexError:
                        current_line = self.current_line
                        raise FormatError("line {!s}: the number of columns "
                            "is less than the number of specifiers"\
                            .format(current_line))

                    if type(value) != type(None):
                        try:
                            value = spec_type(value)
                        except ValueError:
                            current_line = self.current_line
                            raise FormatError("line {!s}: {} is of wrong type"\
                                .format(current_line, def_spec))
 
                    setattr(data, attr, value)

                # Add non-default specifiers to custom_fs attribute
                custom_specs = [i for i in sorted(h, key=h.get, reverse=False) \
                                if i not in def_specs]

                if custom_specs:
                    data.custom_fs = OrderedDict()
                    for key in custom_specs:
                        try:
                            value = spec_values[h[key]]
                        except IndexError:
                            current_line = self.current_line
                            raise FormatError("line {!s}: the number of "
                                "columns is less than the number of "
                                "specifiers".format(current_line))

                        data.custom_fs[key] = value

                line = strip(next_line(handle))  # Raises StopIteration at EOF

                yield data

        except StopIteration:  # Yield last B6/M8 entry
            yield data
