#! /usr/bin/env python

"""Test bio_utils' fasta_verifier

Copyright:

    test_fasta_verifier.py test bio_utils' fasta_verifier
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

from bio_utils.iterators import fasta_iter
from bio_utils.verifiers import fasta_verifier
from bio_utils.verifiers import FormatError
import os

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.0.0'


def test_fasta_verifier():
    """Test bio_utils' fasta_verifier with multiple entries"""

    # Properly formatted set
    entries = r'>entry1{0}AAGGATTCG{0}' \
              r'>entry{0}AGGTCCCCCG{0}' \
              r'>entry3{0}GCCTAGC{0}'.format(os.linesep)

    fasta_entries = fasta_iter(iter(entries.split(os.linesep)))

    # Bad sequence set
    entries2 = r'>entry1{0}AAGGANTCG{0}' \
               r'>entry{0}AGGTCCCCCG{0}' \
               r'>entry3{0}GCCTAGC{0}'.format(os.linesep)

    fasta_entries2 = fasta_iter(iter(entries2.split(os.linesep)))

    # Bad ambiguous-bases sequence set
    entries3 = r'>entry1{0}AAGGAZTCG{0}' \
               r'>entry{0}AGGTCCCCCG{0}' \
               r'>entry3{0}GCCTAGC{0}'.format(os.linesep)

    fasta_entries3 = fasta_iter(iter(entries3.split(os.linesep)))

    # Next two line will throw a FormatError if entry_verifier is broken
    # and doesn't deem entries proper
    fasta_verifier(fasta_entries)
    fasta_verifier(fasta_entries, ambiguous=True)

    # Test bad sequence set
    try:
        fasta_verifier(fasta_entries2)
    except FormatError as error:
        assert error.message == 'entry1 contains a base not in [ACGTU]'

    # Test bad ambiguous-bases sequence set
    try:
        fasta_verifier(fasta_entries3, ambiguous=True)
    except FormatError as error:
        assert error.message == 'entry1 contains a base not in ' \
                                '[ACGTURYKMSWBDHVNX]'

    # Bad header not tested because it is caught by the iterators
