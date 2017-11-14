#! /usr/bin/env python

"""Package containing file verifying functions for biological data

Copyright:

    __init__.py file verifying functions for biological data
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

# First two imports are non-alphabetical because they are required by the
# latter imports.
from bio_utils.verifiers.verify_entries import entry_verifier
from bio_utils.verifiers.verify_entries import FormatError
from bio_utils.verifiers.b6 import b6_verifier
from bio_utils.verifiers.binary import binary_guesser
from bio_utils.verifiers.fasta import fasta_verifier
from bio_utils.verifiers.fastq import fastq_verifier
from bio_utils.verifiers.gff3 import gff3_verifier
from bio_utils.verifiers.sam import sam_verifier

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '2.1.1'
