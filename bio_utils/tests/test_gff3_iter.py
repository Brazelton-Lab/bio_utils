#! /usr/bin/env python

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

from ..iterators import gff3_iter
import os

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.0.0'


# noinspection PyTypeChecker
def test_gff3_iter():
    """Test bio_utils' gff3_iter with multiple GFF3 entries"""

    # Store properly formatted GFF3 data for test gff3_iter
    gff3_data = '##Comment here{0}' \
                'contig1\tProdigal:2.6\tCDS\t6294\t6908\t.\t-\t0\tID=id1;' \
                'Name=name1{0}' \
                'contig2\tProdigal:2.6\tCDS\t7159\t8580\t.\t+\t0\tID=id2;' \
                'Name=name2'.format(os.linesep)

    gff3_handle = iter(gff3_data.split(os.linesep))

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
    assert entries[0].strand == '-'
    assert entries[0].phase == '0'
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
    assert entries[1].score == '.'
    assert entries[1].strand == '+'
    assert entries[1].phase == '0'
    assert entries[1].attributes == 'ID=id2;Name=name2'
    assert entries[1].write() == 'contig2\tProdigal:2.6\tCDS\t7159\t8580\t' \
                                 '.\t+\t0\t' \
                                 'ID=id2;Name=name2{0}'.format(os.linesep)

    # Test gff3_iter's ability to start iterating at arbitrary lines
    gff3_handle = iter(gff3_data.split(os.linesep))  # Reset list iterator

    # Skip comment and first entry
    next(gff3_handle)
    next(gff3_handle)

    header_line = next(gff3_handle)  # Read first line of next entry

    # Obtain next entry with b6_iter
    new_entry = next(gff3_iter(gff3_handle, start_line=header_line))

    # Ensure entry read by gff3_iter is correct
    assert new_entry.seqid == 'contig2'
    assert new_entry.source == 'Prodigal:2.6'
    assert new_entry.type == 'CDS'
    assert new_entry.start == 7159
    assert new_entry.end == 8580
    assert new_entry.score == '.'
    assert new_entry.strand == '+'
    assert new_entry.phase == '0'
    assert new_entry.attributes == 'ID=id2;Name=name2'
    assert new_entry.write() == 'contig2\tProdigal:2.6\tCDS\t7159\t8580\t' \
                                '.\t+\t0\t' \
                                'ID=id2;Name=name2{0}'.format(os.linesep)

    # Repeat everything with prokka option set to true

    gff3_handle = iter(gff3_data.split(os.linesep))  # Reset list iterator

    # Read and store entries
    entries = []
    for entry in gff3_iter(gff3_handle, prokka=True):
        entries.append(entry)

    assert len(entries) == 2  # Ensure gff3_iter read all entries

    # Test first GFF3 entry
    assert entries[0].seqid == 'contig1'
    assert entries[0].source == 'Prodigal:2.6'
    assert entries[0].type == 'CDS'
    assert entries[0].start == 6294
    assert entries[0].end == 6908
    assert entries[0].score == '.'
    assert entries[0].strand == '-'
    assert entries[0].phase == '0'
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
    assert entries[1].score == '.'
    assert entries[1].strand == '+'
    assert entries[1].phase == '0'
    # Next line ensures that the dictionary only contains keys from entry
    assert len(set(entries[1].attributes.keys()) & {'ID', 'Name'}) == 2
    assert entries[1].attributes['ID'] == 'id2'
    assert entries[1].attributes['Name'] == 'name2'
    assert entries[1].write() == 'contig2\tProdigal:2.6\tCDS\t7159\t8580\t' \
                                 '.\t+\t0\t' \
                                 'ID=id2;Name=name2{0}'.format(os.linesep)

    # Test gff3_iter's ability to start iterating at arbitrary lines
    gff3_handle = iter(gff3_data.split(os.linesep))  # Reset list iterator

    # Skip comment first entry
    next(gff3_handle)
    next(gff3_handle)

    header_line = next(gff3_handle)  # Read first line of next entry

    # Obtain next entry with b6_iter
    new_entry = next(gff3_iter(gff3_handle,
                               start_line=header_line,
                               prokka=True))

    # Ensure entry read by gff3_iter is correct
    assert new_entry.seqid == 'contig2'
    assert new_entry.source == 'Prodigal:2.6'
    assert new_entry.type == 'CDS'
    assert new_entry.start == 7159
    assert new_entry.end == 8580
    assert new_entry.score == '.'
    assert new_entry.strand == '+'
    assert new_entry.phase == '0'
    # Next line ensures that the dictionary only contains keys from entry
    assert len(set(new_entry.attributes.keys()) & {'ID', 'Name'}) == 2
    assert new_entry.attributes['ID'] == 'id2'
    assert new_entry.attributes['Name'] == 'name2'
    assert new_entry.write() == 'contig2\tProdigal:2.6\tCDS\t7159\t8580\t' \
                                '.\t+\t0\t' \
                                'ID=id2;Name=name2{0}'.format(os.linesep)
