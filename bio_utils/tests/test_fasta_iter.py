#! /usr/bin/env python

"""Test bio_utils' fasta_iter

Copyright:

    test_fasta_iter.py test bio_utils' fasta_iter
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

from ..iterators import fasta_iter
import os

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.1.0'


# noinspection PyTypeChecker
def test_fasta_iter():
    """Test bio_utils' fasta_iter with multiple unique FASTA entries"""

    # Store various, properly formatted FASTA data for testing fasta_iter
    fasta_data = '>entry1 description1{0}ACCCCGGTTGTGGGACCAAATT{0}' \
                 '>entry2 description2-1 description2-2{0}ACCGAATTTAA{0}' \
                 '>entry3 description3{0}AGGAGGACTTTCG{0}AAGGGTTCG{0}' \
                 '>entry4{0}AAAGGAGAGTTTCCCTTGAG'.format(os.linesep)

    fasta_handle = iter(fasta_data.split(os.linesep))

    # Read and store entries
    entries = []
    for entry in fasta_iter(fasta_handle):
        entries.append(entry)

    assert len(entries) == 4  # Ensure fasta_iter read all entries

    # Test most common use case for FASTA files
    assert entries[0].id == 'entry1'
    assert entries[0].description == 'description1'
    assert entries[0].sequence == 'ACCCCGGTTGTGGGACCAAATT'
    assert entries[0].write() == '>entry1 description1{0}' \
                                 'ACCCCGGTTGTGGGACCAAATT{0}'.format(os.linesep)

    # Test other common use case for FASTA files
    assert entries[1].id == 'entry2'
    assert entries[1].description == 'description2-1 description2-2'
    assert entries[1].sequence == 'ACCGAATTTAA'
    assert entries[1].write() == '>entry2 description2-1 description2-2{0}' \
                                 'ACCGAATTTAA{0}'.format(os.linesep)

    # Test FASTA entry with line-ending separated sequence
    assert entries[2].id == 'entry3'
    assert entries[2].description == 'description3'
    assert entries[2].sequence == 'AGGAGGACTTTCGAAGGGTTCG'
    assert entries[2].write() == '>entry3 description3{0}' \
                                 'AGGAGGACTTTCGAAGGGTTCG{0}'.format(os.linesep)

    # Test FASTA entry with no description
    assert entries[3].id == 'entry4'
    assert entries[3].description == ''
    assert entries[3].sequence == 'AAAGGAGAGTTTCCCTTGAG'
    assert entries[3].write() == '>entry4{0}' \
                                 'AAAGGAGAGTTTCCCTTGAG{0}'.format(os.linesep)

    # Test fasta_iter's ability to start iterating at arbitrary lines
    fasta_handle = iter(fasta_data.split(os.linesep))  # Reset list iterator

    # Skip first entry
    next(fasta_handle)
    next(fasta_handle)

    header_line = next(fasta_handle)  # Read first line of next entry

    # Obtain next entry with fasta_iter
    new_entry = next(fasta_iter(fasta_handle, header=header_line))

    # Ensure entry read by fasta_iter is correct
    assert new_entry.id == 'entry2'
    assert new_entry.description == 'description2-1 description2-2'
    assert new_entry.sequence == 'ACCGAATTTAA'
    assert new_entry.write() == '>entry2 description2-1 description2-2{0}' \
                                'ACCGAATTTAA{0}'.format(os.linesep)
