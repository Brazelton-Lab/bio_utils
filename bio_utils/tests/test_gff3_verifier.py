#! /usr/bin/env python3

"""Test bio_utils' gff3_verifier

Copyright:

    test_gff3_verifier.py test bio_utils' gff3_verifier
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

from bio_utils.iterators import GFF3Entry
from bio_utils.verifiers import FormatError
from bio_utils.verifiers import gff3_verifier

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.0.0'


def test_gff3_verifier():
    """Test bio_utils' gff3_verifier for each error"""

    # Store properly formatted GFF3 data
    entry = GFF3Entry()
    entry.seqid = 'query1'
    entry.source = 'algorithm'
    entry.type = 'CDS'
    entry.start = 1
    entry.end = 50
    entry.score = 750.0
    entry._score_str = '750.0'
    entry.strand = '+'
    entry.phase = 1
    entry.attributes = 'id=hello;'

    # Next two lines should not throw an error unless gff3_verifier is broken
    gff3_verifier([entry])
    gff3_verifier([entry], line=5)

    # Test no seqid
    entry.seqid = ''
    try:
        gff3_verifier([entry])
    except FormatError as error:
        assert error.message == 'Entry with source algorithm has no ' \
                                'Sequence ID'

    # Test no source
    entry.seqid = 'query1'
    entry.source = ''
    try:
        gff3_verifier([entry])
    except FormatError as error:
        assert error.message == 'Entry with Sequence ID query1 has no ' \
                                'source'

    # Test no type
    entry.source = 'subject1'
    entry.type = ''
    try:
        gff3_verifier([entry], line=5)
    except FormatError as error:
        assert error.message == 'Line 5 has non-numerical characters in ' \
                                'type'

    # Test bad start
    entry.type = 'CDS'
    entry.start = 'bad'
    try:
        gff3_verifier([entry])
    except FormatError as error:
        assert error.message == 'Entry with Sequence ID query1 has ' \
                                'non-numerical characters in start position'

    # Test bad end
    entry.start = 1
    entry.end = 'bad'
    try:
        gff3_verifier([entry], line=23)
    except FormatError as error:
        assert error.message == 'Line 23 has non-numerical characters in ' \
                                'end position'

    # Test bad score
    entry.end = 50
    entry._score_str = 'bad'
    try:
        gff3_verifier([entry])
    except FormatError as error:
        assert error.message == 'Entry with Sequence ID query1 has ' \
                                'non-numerical characters in score'

    # Try bad strand
    entry._score_str = '750.0'
    entry.strand = 'bad'
    try:
        gff3_verifier([entry], line=14)
    except FormatError as error:
        assert error.message == 'Line 14 strand not in [+-.]'

    # Test bad phase
    entry.strand = '+'
    entry.phase = 'bad'
    try:
        gff3_verifier([entry])
    except FormatError as error:
        assert error.message == 'Entry with Sequence ID query1 phase not ' \
                                'in [.0-2]'

    # Test no attributes
    entry.phase = 1
    entry.attributes = ''
    try:
        gff3_verifier([entry], line=789)
    except FormatError as error:
        assert error.message == 'Line 789 has no attributes'

    # Test line reading functionality
    entry.attributes = 'id=hello;'

    # Store bad entry
    entry2 = GFF3Entry()
    entry2.seqid = 'query2'
    entry2.source = 'algorithm'
    entry2.type = 'CDS'
    entry2.start = 1
    entry2.end = 50
    entry2.score = 750.0
    entry2._score_str = '750.0'
    entry2.strand = '+'
    entry2.phase = 1
    entry2.attributes = ''

    try:
        gff3_verifier([entry], line=7)
    except FormatError as error:
        assert error.message == 'Line 8 has no attributes'
