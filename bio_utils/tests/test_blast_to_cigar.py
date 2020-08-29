#! /usr/bin/env python3

"""Test bio_utils' blast_to_cigar

Copyright:

    test_blast_to_cigar.py test bio_utils' blast_to_cigar
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

from ..blast_tools import blast_to_cigar

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.0.0'


def test_blast_to_cigar():
    """Test bio_utils' blast_to_cigar with multiple alignments"""

    # Store test data
    query = {
        1: 'AAGGG--CCTTGTA',
        2: 'GGTATA-GCGC',
        3: 'GGTTCTCTCTTCGGGAGGATTTGCTAG'
    }

    subject = {
        1: 'AAGCCTTCCAGGTA',
        2: 'CCTATAG---C',
        3: 'GGTT------TCGGGACCATTTGCTAG'
    }

    alignment_old = {
        1: '|||||  |||||||',
        2: '||||||    |',
        3: '||||      |||||||||||||||||'
    }

    alignment_new = {
        1: 'AAG++  CC++GTA',
        2: '++||||    |',
        3: 'GGTT      TCGGGACCATTTGCTAG'
    }

    # Test first alignment
    assert blast_to_cigar(query[1],
                          alignment_old[1],
                          subject[1],
                          cigar_age='old') == '5M2D7M'
    assert blast_to_cigar(query[1],
                          alignment_new[1],
                          subject[1],
                          cigar_age='new') == '3=2X2D2=2X3='

    # Test second alignment
    assert blast_to_cigar(query[2],
                          alignment_old[2],
                          subject[2],
                          cigar_age='old') == '6MD3IM'
    assert blast_to_cigar(query[2],
                          alignment_new[2],
                          subject[2],
                          cigar_age='new') == '2X4=D3I='

    # Test third alignment
    assert blast_to_cigar(query[3],
                          alignment_old[3],
                          subject[3],
                          cigar_age='old') == '4M6I17M'
    assert blast_to_cigar(query[3],
                          alignment_new[3],
                          subject[3],
                          cigar_age='new') == '4=6I17='
