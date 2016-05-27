#! /usr/bin/env python

"""Returns query sequence from BLAST hits below a specified E-Value

Usage:

    retrieve_query_sequences.py --fastqq <FASTA or FASTQ file>
                                --b6 <B6 or M8 file> --e_value <max E-Value>
                                --output <output file> [--fastq]

Copyright:

    retrieve_query_sequences.py recover query sequence from BLAST alignment
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

import argparse
from bio_utils.iterators import b6_iter
from collections import defaultdict
from bio_utils.iterators import fasta_iter
from bio_utils.iterators import fastq_iter
import sys

__author__ = 'William Brazelton, Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.2.0'


def query_sequence_retriever(fastaq_handle, b6_handle, e_value,
                             fastaq='fasta'):
    """Returns FASTA entries for subject sequences from BLAST hits

    Stores B6/M8 entries with E-Values below the e_value cutoff. Then iterates
    through the FASTA file and if an entry matches the query of an B6/M8
    entry, it's sequence is extracted and returned as a FASTA entry
    plus the E-Value.

    Args:
        fastaq_handle (file): FASTA or FASTQ file handle, can technically
            be any iterable that returns FASTA/Q "lines"

        b6_handle (file): B6/M8 file handle, can technically
            be any iterable that returns FASTA/Q "lines"

        e_value (float): Max E-Value of entry to return

        fastaq (str): ['fasta', 'fastq'] whether file handle is a FASTA or
            FASTQ file

    Yields:
        FastaEntry: class containing all FASTA data
    """

    filtered_b6 = defaultdict(list)
    for entry in b6_iter(b6_handle):
        if float(entry.evalue) <= e_value:
            filtered_b6[entry.query].append(
                (entry.query_start, entry.query_end, entry.evalue))
    fastaq_iter = fasta_iter if fastaq == 'fasta' else fastq_iter
    for fastaqEntry in fastaq_iter(fastaq_handle):
        if fastaqEntry.name in filtered_b6:
            for alignment in filtered_b6[fastaqEntry.name]:
                start = alignment[0] - 1
                end = alignment[1] - 1
                if start < end:
                    query_sequence = fastaqEntry.sequence[start:end]
                elif start > end:
                    query_sequence = fastaqEntry.sequence[end:start][::-1]
                else:
                    query_sequence = fastaqEntry.sequence[start]
                fastaqEntry.sequence = query_sequence
                fastaqEntry.description += ' E-Value: '
                fastaqEntry.description += str(alignment[2])
                yield fastaqEntry


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('--fastaq',
                        type=argparse.FileType('rU'),
                        help='query FASTAQ file')
    parser.add_argument('--b6',
                        type=argparse.FileType('rU'),
                        help='B6/M8 file with alignment data')
    parser.add_argument('--e_value',
                        type=float,
                        help='upper E-Value cutoff')
    parser.add_argument('--fastq',
                        action='store_true',
                        help='specifies that input is FASTQ')
    parser.add_argument('--output',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        nargs='?',
                        help=' optional output file [Default: STDOUT]')
    args = parser.parse_args()

    fastaq = 'fastq' if args.fastq else 'fasta'
    for fastaEntry in query_sequence_retriever(args.fastaq,
                                               args.b6,
                                               args.e_value,
                                               fastaq=fastaq):
        args.output.write(fastaEntry.write())


if __name__ == '__main__':
    main()
    sys.exit(0)
