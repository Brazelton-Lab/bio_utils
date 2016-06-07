#! /usr/bin/env python

"""Test bio_utils' b6_verifier

Copyright:

    test_b6_verifier.py test bio_utils' b6_verifier
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

from bio_utils.iterators import B6Entry
from bio_utils.verifiers import b6_verifier
from bio_utils.verifiers import FormatError

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.1.1'


def test_b6_verifier():
    """Test bio_utils' b6_verifier for each error"""

    # Store properly formatted B6 data
    entry = B6Entry()
    entry.query = 'query1'
    entry.subject = 'subject1'
    entry.perc_identical = 86.03
    entry.align_len = 1782
    entry.mismatches = 226
    entry.gaps = 18
    entry.query_start = 6038
    entry.query_end = 7812
    entry.subject_start = 755762
    entry.subject_end = 753997
    entry.evalue = 0.0
    entry._evalue_str = '0.0'
    entry.bit_score = 1890

    # Next two lines should not throw an error unless b6_verifier is broken
    b6_verifier([entry])
    b6_verifier([entry], line=5)

    # Test no query
    entry.query = ''
    try:
        b6_verifier([entry])
    except FormatError as error:
        assert error.message == 'Entry with subject ID subject1 has ' \
                                'no query ID'

    # Test no subject
    entry.query = 'query1'
    entry.subject = ''
    try:
        b6_verifier([entry])
    except FormatError as error:
        assert error.message == 'Entry with query ID query1 has no ' \
                                'subject ID'

    # Test non-numeric perc_identical
    entry.subject = 'subject1'
    entry.perc_identical = 'bad'
    try:
        b6_verifier([entry], line=5)
    except FormatError as error:
        assert error.message == 'Line 5 has non-numerical characters in ' \
                                'percent identity'

    # Test non-numeric align_len
    entry.perc_identical = 86.03
    entry.align_len = 'bad'
    try:
        b6_verifier([entry])
    except FormatError as error:
        assert error.message == 'Entry with query ID query1 has ' \
                                'non-numerical characters in alignment length'

    # Test non-numeric mismatches
    entry.align_len = 1782
    entry.mismatches = 'bad'
    try:
        b6_verifier([entry])
    except FormatError as error:
        assert error.message == 'Entry with query ID query1 has ' \
                                'non-numerical characters in mismatches'

    # Test non-numeric gaps
    entry.mismatches = 226
    entry.gaps = 'bad'
    try:
        b6_verifier([entry], line=27)
    except FormatError as error:
        assert error.message == 'Line 27 has non-numerical characters in ' \
                                'gaps'

    # Test non-numeric query_start
    entry.gaps = 18
    entry.query_start = 'bad'
    try:
        b6_verifier([entry])
    except FormatError as error:
        assert error.message == 'Entry with query ID query1 has ' \
                                'non-numerical characters in query start'

    # Test non-numeric query_end
    entry.query_start = 6038
    entry.query_end = 'bad'
    try:
        b6_verifier([entry])
    except FormatError as error:
        assert error.message == 'Entry with query ID query1 has ' \
                                'non-numerical characters in query end'

    # Test non-numeric subject_start
    entry.query_end = 7812
    entry.subject_start = 'bad'
    try:
        b6_verifier([entry], line=50)
    except FormatError as error:
        assert error.message == 'Line 50 has non-numerical characters in ' \
                                'subject start'

    # Test non-numeric subject_end
    entry.subject_start = 755762
    entry.subject_end = 'bad'
    try:
        b6_verifier([entry], line=50)
    except FormatError as error:
        assert error.message == 'Line 50 has non-numerical characters in ' \
                                'subject end'

    # Test non-numeric evalue
    entry.subject_end = 753997
    entry._evalue_str = 'bad'
    try:
        b6_verifier([entry])
    except FormatError as error:
        assert error.message == 'Entry with query ID query1 has ' \
                                'non-numerical characters in E-value'

    # Test non-numeric bit_score
    entry._evalue_str = 0.0
    entry.bit_score = 'bad'
    try:
        b6_verifier([entry])
    except FormatError as error:
        assert error.message == 'Entry with query ID query1 has ' \
                                'non-numerical characters in bit score'

    # Test line reading functionality
    entry.bit_score = 1890

    # Store bad entry
    entry2 = B6Entry()
    entry2.query = 'query2'
    entry2.subject = 'subject2'
    entry2.perc_identical = 86.03
    entry2.align_len = 1782
    entry2.mismatches = 226
    entry2.gaps = 18
    entry2.query_start = 6038
    entry2.query_end = 7812
    entry2.subject_start = 755762
    entry2.subject_end = 753997
    entry2.evalue = 0.0
    entry2._evalue_str = '0.0'
    entry2.bit_score = 'bad'

    try:
        b6_verifier([entry, entry2], line=50)
    except FormatError as error:
        assert error.message == 'Line 51 has non-numerical characters in ' \
                                'bit score'
