#! /usr/bin/env python3

"""Test bio_utils' entry_verifier

Copyright:

    test_entry_verifier.py test bio_utils' entry_verifier
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

from bio_utils.verifiers import entry_verifier
from bio_utils.verifiers import FormatError
import os

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.0.0'


def test_entry_verifier():
    """Test bio_utils' entry_verifier with multiple regex and subjects"""

    # Store multiple entries for testing

    # Good data
    regex_solo = r'^>.+{0}[ACGTU]+{0}$'.format(os.linesep)
    subject_solo = '>entry1{0}AGGAATTCGGCTAGCTTGAC{0}'.format(os.linesep)
    delimiter_solo = r'{0}'.format(os.linesep)

    # Bad set 1
    regex_set = r'^@.+\t[ACGTURYKMSWBDHVNX]+\t\+.*\t.+\t$'
    subject_set = [r'@entry1\tAAGGATTCG\t+\t142584412\t'
                   r'@entry\tAGGTZCCCCG\t+\t1224355221\t',
                   r'@entry3\tGCCTAGC\t+\t6443284\t']
    delimiter_set = r'\t'

    # Bad set 2
    regex_set2 = r'^@.+\\r\\n[ACGTURYKMSWBDHVNX]+\\r\\n\+.*\\r\\n.+\\r\\n$'
    subject_set2 = [r'@entry1\r\nAAGGATTCG\r\n+\r\n142584412\r\n'
                    r'@entry\r\nAGGTGCCCCG\r\n+\r\n1224355221\r\n',
                    r'4entry3\r\nGCCTAGC\r\n+\r\n6443284\r\n']
    delimiter_set2 = r'\\r\\n'

    # Next line will throw a FormatError if entry_verifier is broken
    # and doesn't deem subject_solo to match regex_solo
    entry_verifier([subject_solo], regex_solo, delimiter_solo)

    # Test set
    try:
        entry_verifier(subject_set, regex_set, delimiter_set)
    except FormatError as error:
        assert error.template == r'^[ACGTURYKMSWBDHVNX]+$'
        assert error.subject == 'AGGTZCCCCG'
        assert error.part == 1

    # Test set 2
    try:
        entry_verifier(subject_set2, regex_set2, delimiter_set2)
    except FormatError as error:
        assert error.template == r'^@.+$'
        assert error.subject == '4entry3'
        assert error.part == 0
