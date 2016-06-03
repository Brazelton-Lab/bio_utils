#! /usr/bin/env python

"""Test bio_utils' fastq_verifier

Copyright:

    test_fastq_verifier.py test bio_utils' fastq_verifier
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

from bio_utils.iterators import FastqEntry
from bio_utils.verifiers import fastq_verifier
from bio_utils.verifiers import FormatError

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.0.0'


def test_fastq_verifier():
    """Test bio_utils' fastq_verifier with multiple entries"""

    # Store properly formatted FASTQ data
    entry = FastqEntry()
    entry.id = 'entry1'
    entry.description = ''
    entry.sequence = 'AGCGCTTAGCTA'
    entry.quality = '<>_`^[]{}:!"'

    # Next two line won't throw a FormatError unless fastq_verifier is broken
    fastq_verifier([entry])
    fastq_verifier([entry], ambiguous=True)

    # Bad header and line 3 not tested because it is caught by the iterators
    # and added in by FastqEntry.write()

    # Test bad sequence
    entry.sequence = 'AACGCATCGNNG'
    try:
        fastq_verifier([entry])
    except FormatError as error:
        assert error.message == 'entry1 contains a base not in [ACGTU]'

    # Test ambiguous data, no error should be thrown unless broken
    fastq_verifier([entry], ambiguous=True)

    # Test bad ambiguous-bases sequence
    entry.sequence = 'AACGCATCGZZG'
    try:
        fastq_verifier([entry], ambiguous=True)
    except FormatError as error:
        assert error.message == 'entry1 contains a base not in ' \
                                '[ACGTURYKMSWBDHVNX]'

    # Test bad quality score
    entry.sequence = 'AGCGCTTAGCTA'
    entry.quality = '<>_`^[]{}:!\x8e'
    try:
        fastq_verifier([entry])
    except FormatError as error:
        assert error.message == r'entry1 contains a quality score not in ' \
                                r'[!"#$%&\'()*+,-./0123456' \
                                r'789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                                r'[\]^_`abcdefghijklmnopqrstuvwxy' \
                                r'z{|}~]'

    # Test not-equal sequence and quality lengths
    entry.quality = '<>_`^[]{}:!"~='
    try:
        fastq_verifier([entry])
    except FormatError as error:
        assert error.message == 'The number of bases in entry1 does not ' \
                                'match the number of quality scores'
