#! /usr/bin/env python3

"""Test bio_utils' sam_verifier

Copyright:

    test_sam_verifier.py test bio_utils' sam_verifier
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

from bio_utils.iterators import SamEntry
from bio_utils.verifiers import FormatError
from bio_utils.verifiers import sam_verifier

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.0.0'


def test_sam_verifier():
    """Test bio_utils' sam_verifier"""

    # Store properly formatted SAM data
    entry = SamEntry()
    entry.qname = 'query1'
    entry.flag = 4
    entry.rname = 'reference1'
    entry.pos = 73
    entry.mapq = 0
    entry.cigar = '1=3X7='
    entry.rnext = '*'
    entry.pnext = 0
    entry.tlen = 11
    entry.seq = 'ACGT'
    entry.qual = '1234'

    # Next two lines should not throw an error unless sam_verifier is broken
    sam_verifier([entry])
    sam_verifier([entry], line=5)

    # Test no qname
    entry.qname = ''
    try:
        sam_verifier([entry])
    except FormatError as error:
        assert error.message == 'An entry with reference reference1 ' \
                                'has no query name'

    # Test too long qname
    entry.qname = 'a' * 500
    try:
        sam_verifier([entry])
    except FormatError as error:
        assert error.message == 'An entry with reference reference1 query ' \
                                'name must be less than 255 characters'

    # Test bad qname
    entry.qname = '\x8e'
    try:
        sam_verifier([entry])
    except FormatError as error:
        assert error.message == 'An entry with reference reference1 query ' \
                                'name contains characters not in [!-?A-~]'

    # Test bad flag
    entry.qname = 'query1'
    entry.flag = 3E+31
    try:
        sam_verifier([entry])
    except FormatError as error:
        assert error.message == 'An entry with query query1 flag not in ' \
                                'range [0-(2^31-1)]'

    # Test no rname
    entry.flag = 4
    entry.rname = ''
    try:
        sam_verifier([entry])
    except FormatError as error:
        assert error.message == 'An entry with query query1 has no ' \
                                'reference name'

    # Test bad rname
    entry.rname = '\x8e'
    try:
        sam_verifier([entry], line=5)
    except FormatError as error:
        assert error.message == 'Line 5 reference name has characters not ' \
                                'in [!-()+-<>-~][!-~]'

    # Test bad position
    entry.rname = 'reference1'
    entry.pos = 'bad'
    try:
        sam_verifier([entry], line=10)
    except FormatError as error:
        assert error.message == 'Line 10 leftmost position not in range ' \
                                '[0-(2^31-1)]'

    # Test bad mapq
    entry.pos = 73
    entry.mapq = -1
    try:
        sam_verifier([entry])
    except FormatError as error:
        assert error.message == 'An entry with query query1 mapping ' \
                                'quality not in range [0-(2^8-1)]'

    # Test bad CIGAR
    entry.mapq = 0
    entry.cigar = 'Z93T'
    try:
        sam_verifier([entry], line=3)
    except FormatError as error:
        assert error.message == 'Line 3 CIGAR string has characters not in ' \
                                '[0-9MIDNSHPX=]'

    # Test bad rnext
    entry.cigar = '1=3X7='
    entry.rnext = '\x8e'
    try:
        sam_verifier([entry], line=547)
    except FormatError as error:
        assert error.message == 'Line 547 mate read name has characters not ' \
                                'in [!-()+-<>-~][!-~]'

    # Test bad pnext
    entry.rnext = '*'
    entry.pnext = -2
    try:
        sam_verifier([entry])
    except FormatError as error:
        assert error.message == 'An entry with query query1 mate read ' \
                                'position not in range [0-(2^31-1)]'

    # Test bad tlen
    entry.pnext = 0
    entry.tlen = -2E50
    try:
        sam_verifier([entry], line=1500)
    except FormatError as error:
        assert error.message == 'Line 1500 template length not in range ' \
                                '[(-2^31+1)-(2^31-1)]'

    # Test bad seg
    entry.tlen = 11
    entry.seq = '1234'
    try:
        sam_verifier([entry])
    except FormatError as error:
        assert error.message == 'An entry with query query1 sequence has ' \
                                'characters not in [A-Za-z=.]'

    # Test bad qual
    entry.seq = 'ACGT'
    entry.qual = '\x8a\x9f\x2d\x01'
    try:
        sam_verifier([entry], line=1)
    except FormatError as error:
        assert error.message == 'Line 1 quality scores has characters not ' \
                                'in [!-~]'

    # Test line reading functionality
    entry.qual = '1234'

    # Store bad entry
    entry2 = SamEntry()
    entry2.qname = 'query2'
    entry2.flag = 4
    entry2.rname = 'reference2'
    entry2.pos = 'bad'
    entry2.mapq = 0
    entry2.cigar = '1=3X7='
    entry2.rnext = '*'
    entry2.pnext = 0
    entry2.tlen = 11
    entry2.seq = 'ACGT'
    entry2.qual = '1234'

    try:
        sam_verifier([entry], line=10)
    except FormatError as error:
        assert error.message == 'Line 11 leftmost position not in range ' \
                                '[0-(2^31-1)]'
