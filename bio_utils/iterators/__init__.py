#! /usr/bin/env python

"""Import iterators functions and classes at package level

Copyright:

    __init__.py import functions and classes from bio_utils' iterators package
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

from bio_utils.iterators.fasta import fasta_iter
from bio_utils.iterators.fasta import FastaEntry
from bio_utils.iterators.fastq import fastq_iter
from bio_utils.iterators.fastq import FastqEntry
from bio_utils.iterators.gff3 import gff3_iter
from bio_utils.iterators.gff3 import GFF3Entry
from bio_utils.iterators.b6 import b6_iter
from bio_utils.iterators.b6 import B6Entry
from bio_utils.iterators.sam import sam_iter
from bio_utils.iterators.sam import SamEntry

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '2.2.1'
