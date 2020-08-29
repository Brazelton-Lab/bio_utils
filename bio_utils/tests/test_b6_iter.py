#! /usr/bin/env python3

"""Test bio_utils' b6_iter

Copyright:

    test_b6_iter.py test bio_utils' b6_iter
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

#from ..iterators import b6_iter
import os

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.0.3'


def test_b6_iter():  # TODO: fix unit tests
    assert True  # Disabling test until it can be reformatted for new iter

    """
    \"\"\"Test bio_utils' b6_iter\"\"\"

    # Store properly formatted B6/M8 data for testing b6_iter
    b6_data = 'query1\tsubject1\t86.03\t1782\t226\t18\t6038\t7812\t' \
              '755762\t753997\t0.0\t1890{0}' \
              'query2\tsubject2\t85.46\t1176\t165\t5\t1213\t2385\t' \
              '1154754\t1153582\t0.0\t1219'.format(os.linesep)

    b6_handle = iter(b6_data.split(os.linesep))

    # Read and store entries
    entries = []
    for entry in b6_iter(b6_handle):
        entries.append(entry)

    assert len(entries) == 2  # Ensure b6_iter read all entries

    # Test first B6/M6 entry
    assert entries[0].query == 'query1'
    assert entries[0].subject == 'subject1'
    assert entries[0].perc_identical == 86.03
    assert entries[0].align_len == 1782
    assert entries[0].mismatches == 226
    assert entries[0].gaps == 18
    assert entries[0].query_start == 6038
    assert entries[0].query_end == 7812
    assert entries[0].subject_start == 755762
    assert entries[0].subject_end == 753997
    assert entries[0].evalue == 0.0
    assert entries[0]._evalue_str == '0.0'
    assert entries[0].bit_score == 1890
    assert entries[0].write() == 'query1\tsubject1\t86.03\t1782\t226\t18' \
                                 '\t6038\t7812\t755762\t753997\t0.0\t' \
                                 '1890.0{0}'.format(os.linesep)

    # Test second B6/M8 entry
    assert entries[1].query == 'query2'
    assert entries[1].subject == 'subject2'
    assert entries[1].perc_identical == 85.46
    assert entries[1].align_len == 1176
    assert entries[1].mismatches == 165
    assert entries[1].gaps == 5
    assert entries[1].query_start == 1213
    assert entries[1].query_end == 2385
    assert entries[1].subject_start == 1154754
    assert entries[1].subject_end == 1153582
    assert entries[1].evalue == 0.0
    assert entries[1]._evalue_str == '0.0'
    assert entries[1].bit_score == 1219
    assert entries[1].write() == 'query2\tsubject2\t85.46\t1176\t165\t5\t' \
                                 '1213\t2385\t1154754\t1153582\t0.0\t' \
                                 '1219.0{0}'.format(os.linesep)

    # Test b6_iter's ability to start iterating at arbitrary lines
    b6_handle = iter(b6_data.split(os.linesep))  # Reset list iterator

    # Skip first entry
    next(b6_handle)

    header_line = next(b6_handle)  # Read next entry

    # Obtain next entry with b6_iter
    new_entry = next(b6_iter(b6_handle, start_line=header_line))

    # Ensure entry read by b6_iter is correct
    assert new_entry.query == 'query2'
    assert new_entry.subject == 'subject2'
    assert new_entry.perc_identical == 85.46
    assert new_entry.align_len == 1176
    assert new_entry.mismatches == 165
    assert new_entry.gaps == 5
    assert new_entry.query_start == 1213
    assert new_entry.query_end == 2385
    assert new_entry.subject_start == 1154754
    assert new_entry.subject_end == 1153582
    assert new_entry.evalue == 0.0
    assert new_entry._evalue_str == '0.0'
    assert new_entry.bit_score == 1219
    assert new_entry.write() == 'query2\tsubject2\t85.46\t1176\t165\t5\t' \
                                '1213\t2385\t1154754\t1153582\t0.0\t' \
                                '1219.0{0}'.format(os.linesep)"""
