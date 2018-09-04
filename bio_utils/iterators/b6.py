#! /usr/bin/env python

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
__version__ = '5.0.0'


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
        """Return B6/M8 formatted string

        Args:
            default (bool): output entry in default BLAST+ B6 format 

        Returns:
            str: B6/M8 formatted string containing entire B6/M8 entry
        """

        if default:  # Default order of format specifiers
            ordered_vals = ['query', 'subject', 'identity', 'length', 
                            'mismatches', 'gaps', 'query_start', 'query_end', 
                            'subject_start', 'subject_end', 'evalue', 
                            'bitscore']
        else:  # Restore original order of B6 entry format specifiers
            ordered_vals = [self.custom_fs[i] if i in self.custom_fs 
                            else getattr(self, i) for i in self.fs_order]

        fstr = "\t".join(['-' if type(i) == type(None) else i for i in 
                        ordered_vals])

        return '{}{}'.format(fstr, os.linesep)


def b6_iter(handle, start_line=None, header: list=['qaccver', 'saccver', 'pident', 
    'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 
    'evalue', 'bitscore'], comments: bool=False):
    """Iterate over B6/M8 file and return B6/M8 entries

    Args:
        handle (file): B6/M8 file handle, can be any iterator so long as it
            it returns subsequent "lines" of a B6/M8 entry

        start_line (str): Next B6/M8 entry, if 'handle' has been partially read
            and you want to start iterating at the next entry, read the next
            B6/M8 entry and pass it to this variable when  calling b6_iter.
            See 'Examples.'

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
        ...     print(entry.query)  # Print Query ID
        ...     print(entry.subject)  # Print Subject ID
        ...     print(entry.identity)  # Print % identity between seqs
        ...     print(entry.mismatches)  # Print number of mismathces in align
        ...     print(entry.gaps)  # Print number of gaps in alignment
        ...     print(entry.query_start)  # Print start of alignment on query
        ...     print(entry.query_end)  # Print end of alignment on query
        ...     print(entry.subject_start)  # Print start of align on subject
        ...     print(entry.subject_end)  # Print end of alignment on subject
        ...     print(entry.evalue)  # Print E-value of alignment
        ...     print(entry.bitscore)  # Print Bit score of alignment
        ...     print(entry.write())  # Print B6 entry

        >>> b6_handle = open('test.b6out')
        >>> next(b6_handle)  # Skip first line/entry
        >>> next_line = next(b6_handle)  # Store next entry
        >>> for entry in b6_iter(b6_handle, start_line=next_line):
        ...     print(entry.query)  # Print Query ID
        ...     print(entry.subject)  # Print Subject ID
        ...     print(entry.identity)  # Print % identity between seqs
        ...     print(entry.mismatches)  # Print number of mismathces in align
        ...     print(entry.gaps)  # Print number of gaps in alignment
        ...     print(entry.query_start)  # Print start of alignment on query
        ...     print(entry.query_end)  # Print end of alignment on query
        ...     print(entry.subject_start)  # Print start of align on subject
        ...     print(entry.subject_end)  # Print end of alignment on subject
        ...     print(entry.evalue)  # Print E-value of alignment
        ...     print(entry.bitscore)  # Print Bit score of alignment
        ...     print(entry.write())  # Print B6 entry
    """

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
    spec_order = [def_map_rev[i] if i in def_map_rev else i for i in uheader]

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

    # A manual 'for' loop isn't needed to read the file properly and quickly,
    # unlike fasta_iter and fastq_iter, but it is necessary begin iterating
    # partway through a file when the user gives a starting line.
    line_number = 1
    try:  # Manually construct a for loop to improve speed by using 'next'

        while True:  # Loop until StopIteration Exception raised

            line_number += 1

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
                    raise FormatError("the number of columns does not match "
                                      "the number of specifiers in the header "
                                      "at line {!s}".format(line_number))

                if type(value) != type(None):
                    try:
                        value = spec_type(value)
                    except ValueError:
                        raise FormatError("{} is of wrong type at line {!s}"\
                                          .format(def_spec, line_number))
 
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
                        raise FormatError("the number of columns does not match "
                                      "the number of specifiers in the header "
                                      "at line {!s}".format(line_number))

                    data.custom_fs[key] = value

            line = strip(next_line(handle))  # Raises StopIteration at EOF

            yield data

    except StopIteration:  # Yield last B6/M8 entry
        yield data
