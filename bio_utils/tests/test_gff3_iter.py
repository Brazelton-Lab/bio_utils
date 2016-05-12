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
__status__ = 'Alpha'
__version__ = '0.0.1'

def test_gff3_iter():
    """Test bio_utils' gff3_iter with multiple GFF3 entries"""

    # Store properly formatted GFF3 data for test gff3_iter
    gff3_data = 'contig1\tProdigal:2.6\tCDS\t6294\t6908\t.\t-\t0\tID=id1;' \
                'Name=name1;{0}' \
                'contig2\tProdigal:2.6\tCDS\t7159\t8580\t.\t+\t0\tID=id2;' \
                'Name=name2;'.format(os.linesep)

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
    assert entries[0].attributes == 'ID=id1;Name=name1;'
    assert entries[0].write() == 'contig1\tProdigal:2.6\tCDS\t6294\t6908\t' \
                                 '.\t-\t0\t' \
                                 'ID=id1;Name=name1;{0}'.format(os.linesep)
