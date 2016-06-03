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

from bio_utils.iterators import FastaEntry
from bio_utils.verifiers import fasta_verifier
from bio_utils.verifiers import FormatError

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '2.0.0'


def test_fasta_verifier():
    """Test bio_utils' fasta_verifier with multiple entries"""

    # Store properly formatted FASTA data
    entry = FastaEntry()
    entry.id = 'entry1'
    entry.description = ''
    entry.sequence = 'AGCGCTTAGCTA'

    # Next two line won't throw a FormatError unless fasta_verifier is broken
    fasta_verifier([entry])
    fasta_verifier([entry], ambiguous=True)

    # Bad header not tested because it is caught by the iterators
    # and added in by FastaEntry.write()

    # Test bad sequence
    entry.sequence = 'AACGCATCGNNGT'
    try:
        fasta_verifier([entry])
    except FormatError as error:
        assert error.message == 'entry1 contains a base not in [ACGTU]'

    # Test ambiguous data, no error should be thrown unless broken
    fasta_verifier([entry], ambiguous=True)

    # Test bad ambiguous-bases sequence
    entry.sequence = 'AAGAGCTCATATGZZZGZTTAGATCPGG'
    try:
        fasta_verifier([entry], ambiguous=True)
    except FormatError as error:
        assert error.message == 'entry1 contains a base not in ' \
                                '[ACGTURYKMSWBDHVNX]'
