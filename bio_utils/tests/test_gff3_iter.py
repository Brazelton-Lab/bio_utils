#! /usr/bin/env python3

"""Test bio_utils' gff3_iter

Copyright:

    test_gff3_iter.py test bio_utils' gff3_iter
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

#from ..iterators import gff3_iter
import os

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.2.2'


# noinspection PyTypeChecker
def test_gff3_iter():
    assert True  # Disabling test until it can be reformatted for new iter

    """
    \"\"\"Test bio_utils' gff3_iter with multiple GFF3 entries\"\"\"

    # Store properly formatted GFF3 data for testing gff3_iter
    gff3_data = '##gff-version 3.2.1{0}' \
                'contig1\tProdigal:2.6\tCDS\t6294\t6908\t.\t-\t0\tID=id1;' \
                'Name=name1{0}' \
                'contig2\tProdigal:2.6\tCDS\t7159\t8580\t1e5\t+\t.\tID=id2;' \
                'Name=name2{0}' \
                '##FASTA{0}' \
                'ACGT'.format(os.linesep)

    gff3_handle = iter(gff3_data.split(os.linesep))

    # Read and store entries
    entries = []
    for entry in gff3_iter(gff3_handle, parse_attr=False):
        entries.append(entry)

    assert len(entries) == 2  # Ensure gff3_iter read all entries

    # Test first GFF3 entry
    assert entries[0].seqid == 'contig1'
    assert entries[0].source == 'Prodigal:2.6'
    assert entries[0].type == 'CDS'
    assert entries[0].start == 6294
    assert entries[0].end == 6908
    assert entries[0].score == '.'
    assert entries[0]._score_str == '.'
    assert entries[0].strand == '-'
    assert entries[0].phase == 0
    assert entries[0].attributes == 'ID=id1;Name=name1'
    assert entries[0].write() == 'contig1\tProdigal:2.6\tCDS\t6294\t6908\t' \
                                 '.\t-\t0\t' \
                                 'ID=id1;Name=name1{0}'.format(os.linesep)

    # Test second GFF3 entry
    assert entries[1].seqid == 'contig2'
    assert entries[1].source == 'Prodigal:2.6'
    assert entries[1].type == 'CDS'
    assert entries[1].start == 7159
    assert entries[1].end == 8580
    assert entries[1].score == 1e5
    assert entries[1]._score_str == '1e5'
    assert entries[1].strand == '+'
    assert entries[1].phase == '.'
    assert entries[1].attributes == 'ID=id2;Name=name2'
    assert entries[1].write() == 'contig2\tProdigal:2.6\tCDS\t7159\t8580\t' \
                                 '1e5\t+\t.\t' \
                                 'ID=id2;Name=name2{0}'.format(os.linesep)

    # Repeat everything with prokka option set to true

    gff3_handle = iter(gff3_data.split(os.linesep))  # Reset list iterator

    # Read and store entries
    entries = []
    for entry in gff3_iter(gff3_handle):
        entries.append(entry)

    assert len(entries) == 2  # Ensure gff3_iter read all entries

    # Test first GFF3 entry
    assert entries[0].seqid == 'contig1'
    assert entries[0].source == 'Prodigal:2.6'
    assert entries[0].type == 'CDS'
    assert entries[0].start == 6294
    assert entries[0].end == 6908
    assert entries[0].score == '.'
    assert entries[0]._score_str == '.'
    assert entries[0].strand == '-'
    assert entries[0].phase == 0
    # Next line ensures that the dictionary only contains keys from entry
    assert len(set(entries[0].attributes.keys()) & {'ID', 'Name'}) == 2
    assert entries[0].attributes['ID'] == 'id1'
    assert entries[0].attributes['Name'] == 'name1'
    assert entries[0].write() == 'contig1\tProdigal:2.6\tCDS\t6294\t6908\t' \
                                 '.\t-\t0\t' \
                                 'ID=id1;Name=name1{0}'.format(os.linesep)

    # Test second GFF3 entry
    assert entries[1].seqid == 'contig2'
    assert entries[1].source == 'Prodigal:2.6'
    assert entries[1].type == 'CDS'
    assert entries[1].start == 7159
    assert entries[1].end == 8580
    assert entries[1].score == 1e5
    assert entries[1]._score_str == '1e5'
    assert entries[1].strand == '+'
    assert entries[1].phase == '.'
    # Next line ensures that the dictionary only contains keys from entry
    assert len(set(entries[1].attributes.keys()) & {'ID', 'Name'}) == 2
    assert entries[1].attributes['ID'] == 'id2'
    assert entries[1].attributes['Name'] == 'name2'
    assert entries[1].write() == 'contig2\tProdigal:2.6\tCDS\t7159\t8580\t' \
                                 '1e5\t+\t.\t' \
                                 'ID=id2;Name=name2{0}'.format(os.linesep)

    # Repeat everything with headers option set to true

    gff3_handle = iter(gff3_data.split(os.linesep))  # Reset list iterator

    # Read and store entries
    entries = []
    for entry in gff3_iter(gff3_handle, parse_attr=False, headers=True):
        entries.append(entry)

    assert len(entries) == 3  # Ensure gff3_iter read header and all entries

    # Test header
    assert entries[0] == '##gff-version 3.2.1'

    # Test first GFF3 entry
    assert entries[1].seqid == 'contig1'
    assert entries[1].source == 'Prodigal:2.6'
    assert entries[1].type == 'CDS'
    assert entries[1].start == 6294
    assert entries[1].end == 6908
    assert entries[1].score == '.'
    assert entries[1]._score_str == '.'
    assert entries[1].strand == '-'
    assert entries[1].phase == 0
    assert entries[1].attributes == 'ID=id1;Name=name1'
    assert entries[1].write() == 'contig1\tProdigal:2.6\tCDS\t6294\t6908\t' \
                                 '.\t-\t0\t' \
                                 'ID=id1;Name=name1{0}'.format(os.linesep)

    # Test second GFF3 entry
    assert entries[2].seqid == 'contig2'
    assert entries[2].source == 'Prodigal:2.6'
    assert entries[2].type == 'CDS'
    assert entries[2].start == 7159
    assert entries[2].end == 8580
    assert entries[2].score == 1e5
    assert entries[2]._score_str == '1e5'
    assert entries[2].strand == '+'
    assert entries[2].phase == '.'
    assert entries[2].attributes == 'ID=id2;Name=name2'
    assert entries[2].write() == 'contig2\tProdigal:2.6\tCDS\t7159\t8580\t' \
                                 '1e5\t+\t.\t' \
                                 'ID=id2;Name=name2{0}'.format(os.linesep)

    # Test gff3_iter's ability to start iterating at an arbitrary line
    gff3_handle = iter(gff3_data.split(os.linesep))  # Reset list iterator

    # Skip comment first entry
    next(gff3_handle)
    next(gff3_handle)

    header_line = next(gff3_handle)  # Read first line of next entry

    # Obtain next entry with b6_iter
    new_entry = next(gff3_iter(gff3_handle,
                               start_line=header_line))

    # Ensure entry read by gff3_iter is correct
    assert new_entry.seqid == 'contig2'
    assert new_entry.source == 'Prodigal:2.6'
    assert new_entry.type == 'CDS'
    assert new_entry.start == 7159
    assert new_entry.end == 8580
    assert new_entry.score == 1e5
    assert new_entry._score_str == '1e5'
    assert new_entry.strand == '+'
    assert new_entry.phase == '.'
    # Next line ensures that the dictionary only contains keys from entry
    assert len(set(new_entry.attributes.keys()) & {'ID', 'Name'}) == 2
    assert new_entry.attributes['ID'] == 'id2'
    assert new_entry.attributes['Name'] == 'name2'
    assert new_entry.write() == 'contig2\tProdigal:2.6\tCDS\t7159\t8580\t' \
                                '1e5\t+\t.\t' \
                                'ID=id2;Name=name2{0}'.format(os.linesep)

    # Test gff3_iter's ability to start iterating at arbitrary lines
    gff3_handle = iter(gff3_data.split(os.linesep))  # Reset list iterator

    # Skip comment and first entry
    next(gff3_handle)
    next(gff3_handle)

    header_line = next(gff3_handle)  # Read next entry

    # Obtain next entry with gff3_iter
    new_entry = next(gff3_iter(gff3_handle,
                               parse_attr=False,
                               start_line=header_line))

    # Ensure entry read by gff3_iter is correct
    assert new_entry.seqid == 'contig2'
    assert new_entry.source == 'Prodigal:2.6'
    assert new_entry.type == 'CDS'
    assert new_entry.start == 7159
    assert new_entry.end == 8580
    assert new_entry.score == 1e5
    assert new_entry._score_str == '1e5'
    assert new_entry.strand == '+'
    assert new_entry.phase == '.'
    assert new_entry.attributes == 'ID=id2;Name=name2'
    assert new_entry.write() == 'contig2\tProdigal:2.6\tCDS\t7159\t8580\t' \
                                '1e5\t+\t.\t' \
                                'ID=id2;Name=name2{0}'.format(os.linesep)"""
