#! /usr/bin/env python3

"""Test bio_utils' sam_iter

Copyright:

    test_sam_iter.py test bio_utils' sam_iter
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

from ..iterators import sam_iter
import os

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.0.0'


# noinspection PyTypeChecker
def test_sam_iter():
    """Test bio_utils' sam_iter with multiple SAM entries"""

    # Store properly formatted SAM data for testing sam_iter
    sam_data = '@HD{0}' \
               'HISEQ03:358:D27UGACXX:4:1101:7778:74412\t2\tcontig-0\t' \
               '1\t6\t4M11I135M\t=\t113\t262\tAGCCACTGGGTTGATTTGGCA\t'\
               'BCCFFFFFHHDFHGIJJGJIJ{0}' \
               'HISEQ03:358:D27UGACXX:4:1203:13071:100297\t0x2\tcontig-0\t' \
               '1\t42\t130M\t=\t315\t433\tTGATTTGGCAAAAGACAATTCA\t' \
               '=?;DDDBFGFFHFGGIIGGIGH'.format(os.linesep)

    sam_handle = iter(sam_data.split(os.linesep))

    # Read and store entries
    entries = []
    for entry in sam_iter(sam_handle):
        entries.append(entry)

    assert len(entries) == 2  # Ensure sam_iter read all entries

    # Test first SAM entry
    assert entries[0].qname == 'HISEQ03:358:D27UGACXX:4:1101:7778:74412'
    assert entries[0].flag == 2
    assert entries[0].rname == 'contig-0'
    assert entries[0].pos == 1
    assert entries[0].mapq == 6
    assert entries[0].cigar == '4M11I135M'
    assert entries[0].rnext == '='
    assert entries[0].pnext == 113
    assert entries[0].tlen == 262
    assert entries[0].seq == 'AGCCACTGGGTTGATTTGGCA'
    assert entries[0].qual == 'BCCFFFFFHHDFHGIJJGJIJ'
    assert entries[0].write() == 'HISEQ03:358:D27UGACXX:4:1101:7778:74412\t' \
                                 '2\tcontig-0\t1\t6\t4M11I135M\t=\t113\t' \
                                 '262\tAGCCACTGGGTTGATTTGGCA\t'\
                                 'BCCFFFFFHHDFHGIJJGJIJ{0}'.format(os.linesep)

    # Test second SAM entry
    assert entries[1].qname == 'HISEQ03:358:D27UGACXX:4:1203:13071:100297'
    assert entries[1].flag == '0x2'
    assert entries[1].rname == 'contig-0'
    assert entries[1].pos == 1
    assert entries[1].mapq == 42
    assert entries[1].cigar == '130M'
    assert entries[1].rnext == '='
    assert entries[1].pnext == 315
    assert entries[1].tlen == 433
    assert entries[1].seq == 'TGATTTGGCAAAAGACAATTCA'
    assert entries[1].qual == '=?;DDDBFGFFHFGGIIGGIGH'
    assert entries[1].write() == 'HISEQ03:358:D27UGACXX:4:1203:13071:100297' \
                                 '\t0x2\tcontig-0\t1\t42\t130M\t=\t315\t433' \
                                 '\tTGATTTGGCAAAAGACAATTCA\t' \
                                 '=?;DDDBFGFFHFGGIIGGIGH{0}'.format(os.linesep)

    # Repeat everything with headers option set to true

    sam_handle = iter(sam_data.split(os.linesep))  # Reset list iterator

    # Read and store entries
    entries = []
    for entry in sam_iter(sam_handle, headers=True):
        entries.append(entry)

    assert len(entries) == 3  # Ensure sam_iter read header and all entries

    # Test header
    assert entries[0] == '@HD'

    # Test first SAM entry
    assert entries[1].qname == 'HISEQ03:358:D27UGACXX:4:1101:7778:74412'
    assert entries[1].flag == 2
    assert entries[1].rname == 'contig-0'
    assert entries[1].pos == 1
    assert entries[1].mapq == 6
    assert entries[1].cigar == '4M11I135M'
    assert entries[1].rnext == '='
    assert entries[1].pnext == 113
    assert entries[1].tlen == 262
    assert entries[1].seq == 'AGCCACTGGGTTGATTTGGCA'
    assert entries[1].qual == 'BCCFFFFFHHDFHGIJJGJIJ'
    assert entries[1].write() == 'HISEQ03:358:D27UGACXX:4:1101:7778:74412\t' \
                                 '2\tcontig-0\t1\t6\t4M11I135M\t=\t113\t' \
                                 '262\tAGCCACTGGGTTGATTTGGCA\t' \
                                 'BCCFFFFFHHDFHGIJJGJIJ{0}'.format(os.linesep)

    # Test second SAM entry
    assert entries[2].qname == 'HISEQ03:358:D27UGACXX:4:1203:13071:100297'
    assert entries[2].flag == '0x2'
    assert entries[2].rname == 'contig-0'
    assert entries[2].pos == 1
    assert entries[2].mapq == 42
    assert entries[2].cigar == '130M'
    assert entries[2].rnext == '='
    assert entries[2].pnext == 315
    assert entries[2].tlen == 433
    assert entries[2].seq == 'TGATTTGGCAAAAGACAATTCA'
    assert entries[2].qual == '=?;DDDBFGFFHFGGIIGGIGH'
    assert entries[2].write() == 'HISEQ03:358:D27UGACXX:4:1203:13071:100297' \
                                 '\t0x2\tcontig-0\t1\t42\t130M\t=\t315\t433' \
                                 '\tTGATTTGGCAAAAGACAATTCA\t' \
                                 '=?;DDDBFGFFHFGGIIGGIGH{0}'.format(os.linesep)

    # Test sam_iter's ability to start iterating at an arbitrary line
    sam_handle = iter(sam_data.split(os.linesep))  # Reset list iterator

    # Skip header and first entry
    next(sam_handle)
    next(sam_handle)

    header_line = next(sam_handle)  # Read next entry

    # Obtain next entry with sam_iter
    new_entry = next(sam_iter(sam_handle, start_line=header_line))

    # Ensure entry read by sam_iter is correct
    assert new_entry.qname == 'HISEQ03:358:D27UGACXX:4:1203:13071:100297'
    assert new_entry.flag == '0x2'
    assert new_entry.rname == 'contig-0'
    assert new_entry.pos == 1
    assert new_entry.mapq == 42
    assert new_entry.cigar == '130M'
    assert new_entry.rnext == '='
    assert new_entry.pnext == 315
    assert new_entry.tlen == 433
    assert new_entry.seq == 'TGATTTGGCAAAAGACAATTCA'
    assert new_entry.qual == '=?;DDDBFGFFHFGGIIGGIGH'
    assert new_entry.write() == 'HISEQ03:358:D27UGACXX:4:1203:13071:100297' \
                                '\t0x2\tcontig-0\t1\t42\t130M\t=\t315\t433' \
                                '\tTGATTTGGCAAAAGACAATTCA\t' \
                                '=?;DDDBFGFFHFGGIIGGIGH{0}'.format(os.linesep)
