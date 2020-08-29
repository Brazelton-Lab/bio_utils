#! /usr/bin/env python3

"""Test bio_utils' query_sequence_retriever

Copyright:

    test_query_sequence_retriever.py test bio_utils' query_sequence_retriever
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

from ..blast_tools import query_sequence_retriever
import os

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.0.2'


def test_query_sequence_retiever():  # TODO: fix unit tests
    assert True  # Disabling test until it can be reformatted for new iter

    """
    \"\"\"Test bio_utils' query_sequence_retriever\"\"\"

    # Store properly formatted B6/M8 data
    b6_data = 'query1\tsubject1\t86.03\t10\t3\t1\t15\t5\t' \
              '100\t115\t1E-5\t1890{0}' \
              'query2\tsubject2\t95.46\t23\t5\t7\t10\t33\t' \
              '50\t73\t3E-0\t1219{0}' \
              'query3\tsubject3\t85.46\t13\t2\t5\t10\t23\t' \
              '50\t63\t1E-37\t1219'.format(os.linesep)

    b6_handle = iter(b6_data.split(os.linesep))

    # Store properly formatted FASTA data
    fasta_data = '>query1{0}AGGCTAGGCTAGCTGGTCAAGGCT{0}' \
                 '>query3 description{0}AAGGGCGCTTGCGAGCTTAGCTAGAGCTAGGCTA' \
                 .format(os.linesep)

    fasta_handle = iter(fasta_data.split(os.linesep))

    # Store properly formatted FASTQ data
    fastq_data = '@query1{0}AGGCTAGGCTAGCTGGTCAAGGCT{0}+{0}' \
                 '122345442123432212334432{0}' \
                 '@query3 description{0}AAGGGCGCTTGCGAGCTTAGCTAGAGCTAGGCTA' \
                 '{0}+{0}7788203944532012337548391092833451'.format(os.linesep)

    fastq_handle = iter(fastq_data.split(os.linesep))

    entries = []
    for entry in query_sequence_retriever(fasta_handle, b6_handle, 1):
        entries.append(entry)

    assert len(entries) == 2  # Ensure high E-value entry dropped

    # Test first entry with reverse sequence alignment (start: 15, end: 5)
    assert entries[0].id == 'query1'
    assert entries[0].description == 'E-value: 1E-5'
    assert entries[0].sequence == 'TCGATCGGAT'
    assert entries[0].write() == '>query1 E-value: 1E-5{0}' \
                                 'TCGATCGGAT{0}'.format(os.linesep)

    # Test second entry with description
    assert entries[1].id == 'query3'
    assert entries[1].description == 'description E-value: 1E-37'
    assert entries[1].sequence == 'TGCGAGCTTAGCT'
    assert entries[1].write() == '>query3 description E-value: 1E-37{0}' \
                                 'TGCGAGCTTAGCT{0}'.format(os.linesep)

    # Test everything again with FASTQ data
    b6_handle = iter(b6_data.split(os.linesep))  # Reset handle
    entries = []
    for entry in query_sequence_retriever(fastq_handle, b6_handle, 1,
                                          fastaq='fastq'):
        entries.append(entry)

    assert len(entries) == 2  # Ensure high E-value entry dropped

    # Test first entry with reverse sequence alignment (start: 15, end: 5)
    assert entries[0].id == 'query1'
    assert entries[0].description == 'E-value: 1E-5'
    assert entries[0].sequence == 'TCGATCGGAT'
    assert entries[0].quality == '3432124454'
    assert entries[0].write() == '@query1 E-value: 1E-5{0}' \
                                 'TCGATCGGAT{0}+{0}' \
                                 '3432124454{0}'.format(os.linesep)

    # Test second entry with description
    assert entries[1].id == 'query3'
    assert entries[1].description == 'description E-value: 1E-37'
    assert entries[1].sequence == 'TGCGAGCTTAGCT'
    assert entries[1].write() == '@query3 description E-value: 1E-37{0}' \
                                 'TGCGAGCTTAGCT{0}+{0}' \
                                 '4532012337548{0}'.format(os.linesep)"""
