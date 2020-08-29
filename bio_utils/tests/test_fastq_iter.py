#! /usr/bin/env python3

"""Test bio_utils' fastq_iter

Copyright:

    test_fastq_iter.py test bio_utils' fastq_iter
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

from ..iterators import fastq_iter
import os

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.0.0'


# noinspection PyTypeChecker
def test_fastq_iter():
    """Test bio_utils' fastq_iter with multiple unique FASTQ entries"""

    # Store various, properly formatted FASTQ data for testing fastq_iter
    fastq_data = '@entry1 description1{0}GGTTTCATCAG{0}+{0}@!"""()()(*{0}' \
                 '@entry2 description2-1 description2-2{0}TTGGCAT{0}+{0}' \
                 '<=>(123{0}' \
                 '@entry3 description3{0}TTGGTAC{0}GGA{0}+{0}$$&&68A{0}EDG{0}'\
                 '@entry4{0}GGATTCGATA{0}+{0}[]%%%@@345{0}' \
                 '@entry5 description5{0}TTAGGC{0}+ entry5 description5{0}' \
                 '555555'.format(os.linesep)

    fastq_handle = iter(fastq_data.split(os.linesep))

    # Read and store entries
    entries = []
    for entry in fastq_iter(fastq_handle):
        entries.append(entry)

    assert len(entries) == 5  # Ensure fastq_iter read all entries

    # Test most common use case for FASTQ files
    assert entries[0].id == 'entry1'
    assert entries[0].description == 'description1'
    assert entries[0].sequence == 'GGTTTCATCAG'
    assert entries[0].quality == '@!"""()()(*'
    assert entries[0].write() == '@entry1 description1{0}GGTTTCATCAG{0}+{0}' \
                                 '@!"""()()(*{0}'.format(os.linesep)

    # Test other common use case for FASTQ files
    assert entries[1].id == 'entry2'
    assert entries[1].description == 'description2-1 description2-2'
    assert entries[1].sequence == 'TTGGCAT'
    assert entries[1].quality == '<=>(123'
    assert entries[1].write() == '@entry2 description2-1 description2-2{0}' \
                                 'TTGGCAT{0}+{0}<=>(123{0}'.format(os.linesep)

    # Test FASTQ entries with line-separated sequences and quality
    assert entries[2].id == 'entry3'
    assert entries[2].description == 'description3'
    assert entries[2].sequence == 'TTGGTACGGA'
    assert entries[2].quality == '$$&&68AEDG'
    assert entries[2].write() == '@entry3 description3{0}TTGGTACGGA{0}+{0}' \
                                 '$$&&68AEDG{0}'.format(os.linesep)

    # Test FASTQ entry with no description
    assert entries[3].id == 'entry4'
    assert entries[3].description == ''
    assert entries[3].sequence == 'GGATTCGATA'
    assert entries[3].quality == '[]%%%@@345'
    assert entries[3].write() == '@entry4{0}GGATTCGATA{0}+{0}' \
                                 '[]%%%@@345{0}'.format(os.linesep)

    # Test FASTQ entry with ID and Description on third line with '+'
    assert entries[4].id == 'entry5'
    assert entries[4].description == 'description5'
    assert entries[4].sequence == 'TTAGGC'
    assert entries[4].quality == '555555'
    assert entries[4].write() == '@entry5 description5{0}TTAGGC{0}+{0}' \
                                 '555555{0}'.format(os.linesep)

    # Test fastq_iter's ability to start iterating at arbitrary lines
    fastq_handle = iter(fastq_data.split(os.linesep))  # Reset list iterator

    # Skip first entry
    next(fastq_handle)
    next(fastq_handle)
    next(fastq_handle)
    next(fastq_handle)

    header_line = next(fastq_handle)  # Read first line of next entry

    # Obtain next entry with fastq_iter
    new_entry = next(fastq_iter(fastq_handle, header=header_line))

    # Ensure entry read by fastq_iter
    assert new_entry.id == 'entry2'
    assert new_entry.description == 'description2-1 description2-2'
    assert new_entry.sequence == 'TTGGCAT'
    assert new_entry.quality == '<=>(123'
    assert new_entry.write() == '@entry2 description2-1 description2-2{0}' \
                                'TTGGCAT{0}+{0}<=>(123{0}'.format(os.linesep)
