#! /usr/bin/env python

"""Iterator for GFF3 files

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
__version__ = '3.1.3'


class FastaFound(Exception):
    """A simple exception to prevent iterating over FASTA file in GFF3 file"""

    def __init__(self):
        """This exception acts as a flag for iteration and nothing more"""

        pass


class GFF3Entry:
    """A simple class to store data from GFF3 entries and write them

    Attributes:
        seqid (str): ID of sequence annotated

        source (str): what performed annotation

        type (str): type of feature (CDS, rRNA, etc.)

        start (int): start of feature

        end (int): end of feature

        score (float): score/confidence of feature, often a P-value, returns
            str "." if no score given

        strand (str): [+, -, .] strand that feature is located on

        phase (int): int if phase given in file, else str. Required for
            features of type "CDS," indicates bases until next codon in feature

        attributes (dict): OrderedDict if prase_attr is True, else str. Various
            attributes formatted as "<tag>=<value>" with multiple attributes
            separated by semicolons. If parse_attr true, creates dict where
            tags are keys and values are values as follows (in YAML format):

            Original String: tag1=value1;tag2=value2

            {
            tag1: value1,
            tag2: value2
            }
    """

    def __init__(self):
        """Initialize variables to store GFF3 entry data"""

        self.seqid = None
        self.source = None
        self.type = None
        self.start = None
        self.end = None
        self.score = None
        self._score_str = None  # Original formatting
        self.strand = None
        self.phase = None
        self.attributes = None
        self._temp_attributes = None  # Used in case attributes is dict

    def write(self):
        """Return GFF3 formatted string

        Returns:
            str: GFF3 formatted string containing entire GFF3 entry
        """

        # Regain original formatting for GFF file
        if type(self.attributes) is OrderedDict:
            self._temp_attributes = ''
            for key, value in self.attributes.items():
                self._temp_attributes += '{0}={1};'.format(key, value)
            self._temp_attributes = self._temp_attributes[:-1]
        else:
            self._temp_attributes = self.attributes

        return '{0}\t{1}\t{2}\t{3}\t{4}\t' \
               '{5}\t{6}\t{7}\t{8}{9}'.format(self.seqid,
                                              self.source,
                                              self.type,
                                              str(self.start),
                                              str(self.end),
                                              self._score_str,
                                              self.strand,
                                              self.phase,
                                              self._temp_attributes,
                                              os.linesep)


def gff3_iter(handle, start_line=None, parse_attr=True, headers=False):
    """Iterate over GFF3 file and return GFF3 entries

    Args:
        handle (file): GFF3 file handle, can be any iterator so long as it
            it returns subsequent "lines" of a GFF3 entry

        start_line (str): Next GFF3 entry, if 'handle' has been partially read
            and you want to start iterating at the next entry, read the next
            GFF3 entry and pass it to this variable when calling gff3_iter.
            See 'Examples.'

        parse_attr (bool): Parse attributes column into a dictionary such that
            the string "tag1=value1;tag2=value2" becomes (in YAML format):

            tag1: value1
            tag2: value2

        headers (bool): Yields headers if True, else skips lines starting with
            "##"

    Yields:
        GFF3Entry: class containing all GFF3 data, yields str for headers if
            headers options is True then yields GFF3Entry for entries

    Examples:
        The following three examples demonstrate how to use gff3_iter.
        Note: These doctests will not pass, examples are only in doctest
        format as per convention. bio_utils uses pytests for testing.

        >>> for entry in gff3_iter(open('test.gff3')):
        ...     print(entry.seqid)  # Print Sequence ID
        ...     print(entry.source)  # Print software that performed annotation
        ...     print(entry.type)  # Print type of annotation
        ...     print(entry.start)  # Print start position of annotation
        ...     print(entry.end)  # Print end position of annotation
        ...     print(entry.score)  # Print confidence score of annotation
        ...     print(entry.strand)  # Print strand annotation is on
        ...     print(entry.phase)  # Print bases until next codon
        ...     print(entry.attributes)  # Print attributes of annotation
        ...     print(entry.write())  # Print entry GFF3 entry

        >>> gff3_handle = open('test.gff3')
        >>> next(gff3_handle)  # Skip first line/entry
        >>> next_line = next(gff3_handle)  # Store next entry
        >>> for entry in gff3_iter(gff3_handle, start_line=next_line):
        ...     print(entry.seqid)  # Print Sequence ID
        ...     print(entry.source)  # Print software that performed annotation
        ...     print(entry.type)  # Print type of annotation
        ...     print(entry.start)  # Print start position of annotation
        ...     print(entry.end)  # Print end position of annotation
        ...     print(entry.score)  # Print confidence score of annotation
        ...     print(entry.strand)  # Print strand annotation is on
        ...     print(entry.phase)  # Print bases until next codon
        ...     print(entry.attributes)  # Print attributes of annotation
        ...     print(entry.write())  # Print entry GFF3 entry

        >>> for entry in gff3_iter(open('test.gff3'), parse_attr=True):
        ...     print(entry.seqid)  # Print Sequence ID
        ...     print(entry.source)  # Print software that performed annotation
        ...     print(entry.type)  # Print type of annotation
        ...     print(entry.start)  # Print start position of annotation
        ...     print(entry.end)  # Print end position of annotation
        ...     print(entry.score)  # Print confidence score of annotation
        ...     print(entry.strand)  # Print strand annotation is on
        ...     print(entry.phase)  # Print bases until next codon
        ...     print(entry.attributes['attr1'])  # Print attribute 'attr1'
        ...     print(entry.attributes['attr2'])  # Print attribute 'attr2'
        ...     print(entry.write())  # Print entry GFF3 entry
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

            data = GFF3Entry()  # Initialize early to prevent access error

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

            data.seqid = split_line[0]
            data.source = split_line[1]
            data.type = split_line[2]
            data.start = int(split_line[3])
            data.end = int(split_line[4])
            try:  # Make float unless dot
                data.score = float(split_line[5])
            except ValueError:
                data.score = split_line[5]
            data._score_str = split_line[5]
            data.strand = split_line[6]
            try:  # Get phase as int unless phase not given
                data.phase = int(split_line[7])
            except ValueError:
                data.phase = split_line[7]
            data.attributes = split_line[8]

            if parse_attr:
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
    except FastaFound:  # When FASTA found, last entry is repeat so pass
        pass
