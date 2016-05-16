#!/usr/bin/env python

"""Screed-esque iterator for GFF3 files

Copyright:

    gff3.py iterate over and return entries of a GFF3 file
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

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '2.1.0'


class FastaFound(Exception):
    """A simple exception to prevent iterating over FASTA file in GFF3 file"""

    def __init__(self):
        pass


class GFF3Entry:
    """A simple class to store data from GFF3 entries and write them"""

    def __init__(self):
        """Initialize variables to store GFF3 entry data"""

        self.seqid = None
        self.source = None
        self.type = None
        self.start = None
        self.end = None
        self.score = None
        self.strand = None
        self.phase = None
        self.attributes = None
        self.temp_attributes = None  # Used in case attributes is dict

    def write(self):
        """Return GFF3 formatted string

        :return: GFF3 formatted string
        :rtype: str
        """

        # Regain original formatting for GFF file
        if type(self.attributes) is OrderedDict:
            self.temp_attributes = ''
            for key, value in self.attributes.items():
                self.temp_attributes += '{0}={1};'.format(key, value)
            self.temp_attributes = self.temp_attributes[:-1]
        else:
            self.temp_attributes = self.attributes

        return '{0}\t{1}\t{2}\t{3}\t{4}\t' \
               '{5}\t{6}\t{7}\t{8}{9}'.format(self.seqid,
                                              self.source,
                                              self.type,
                                              str(self.start),
                                              str(self.end),
                                              self.score,
                                              self.strand,
                                              self.phase,
                                              self.temp_attributes,
                                              os.linesep)


def gff3_iter(handle, start_line=None, prokka=False, headers=False):
    """Iterate over GFF3 file and return GFF3 entries

    PROKKA option parses attributes column of GFF3 files from PROKKA version
    1.12-beta. As an example, it parses:

    prokka_id=5;gene_id=example_id

    into an ordered dictionary as follows in YAML format:

    prokka_id: 5
    gene_id: example_id

    and stores it as the 'attributes' attribute of the returned class.

    :param handle: GFF3 file handle, can technically be any iterator
    :type handle: File Object

    :param start_line: Header line of entry file handle is open to
    :type start_line: str

    :param prokka: Dynamically parse attributes column of PROKKA 1.12-beta
    :type: boolean

    :return: class containing GFF3 data
    :rtype: GFF3Entry

    :param headers: True returns header lines, False skips them
    :type headers: bool
    """

    # Speed tricks: reduces function calls
    split = str.split
    strip = str.strip

    if start_line is None:
        line = strip(next(handle))  # Read first GFF3 entry
    else:
        line = strip(start_line)  # Set header to given header

    # A manual 'for' loop isn't needed to read the file properly and quickly,
    # unlike fasta_iter and fastq_iter, but it is necessary begin iterating
    # partway through a file when the user gives a starting line.
    try:  # Manually construct a for loop to improve speed by using 'next'

        while True:  # Loop until StopIteration Exception raised

            if line.startswith('##FASTA'):  # Skip FASTA entries
                raise FastaFound

            if line.startswith('##') and not headers:
                line = strip(next(handle))
                continue
            elif line.startswith('##') and headers:
                yield line
                line = strip(next(handle))
                continue

            split_line = split(line, '\t')

            data = GFF3Entry()
            data.seqid = split_line[0]
            data.source = split_line[1]
            data.type = split_line[2]
            data.start = int(split_line[3])
            data.end = int(split_line[4])
            data.score = split_line[5]  # Kept as str to preserve formatting
            data.strand = split_line[6]
            try: # Get phase as int unless phase not given
                data.phase = int(split_line[7])
            except ValueError:
                data.phase = split_line[7]
            data.attributes = split_line[8]

            if prokka:
                attributes = split(data.attributes, ';')
                data.attributes = OrderedDict()
                for attribute in attributes:
                    split_attribute = attribute.split('=')
                    key = split_attribute[0]
                    value = split_attribute[-1]
                    if not key == '':  # Avoid semicolon split at end of line
                        data.attributes[key] = value

            line = strip(next(handle))  # Raises StopIteration at EOF

            yield data

    except StopIteration:  # Yield last GFF3 entry
        yield data
    except FastaFound:  # When FASTA found, last entry is repeat
        pass
