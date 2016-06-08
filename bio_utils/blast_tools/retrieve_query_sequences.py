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
from bio_utils.blast_tools import b6_evalue_filter
from bio_utils.iterators import fasta_iter
from bio_utils.iterators import fastq_iter
from collections import defaultdict
import sys

__author__ = 'William Brazelton, Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '2.0.0'


def query_sequence_retriever(fastaq_handle, b6_handle, e_value,
                             fastaq='fasta', *args, **kwargs):
    """Returns FASTA entries for subject sequences from BLAST hits

    Stores B6/M8 entries with E-Values below the e_value cutoff. Then iterates
    through the FASTA file and if an entry matches the query of an B6/M8
    entry, it's sequence is extracted and returned as a FASTA entry
    plus the E-Value.

    Args:
        fastaq_handle (file): FASTA or FASTQ file handle, can technically
            be any iterable that returns FASTA/Q "lines"

        b6_handle (file): B6/M8 file handle, can technically
            be any iterable that returns B6/M8"lines"

        e_value (float): Max E-Value of entry to return

        fastaq (str): ['fasta', 'fastq'] whether file handle is a FASTA or
            FASTQ file

        *args: Variable length argument list for b6_iter

        **kwargs: Arbitrary keyword arguments for b6_iter

    Yields:
        FastaEntry: class containing all FASTA data
            FastqEntry if fastaq='fastq'

    Example:
        Note: These doctests will not pass, examples are only in doctest
        format as per convention. bio_utils uses pytests for testing.

        >>> fasta_handle = open('test.fasta')
        >>> b6_handle = open('test.b6')
        >>> for entry in query_sequence_retriever(fasta_handle,
        ...                                       b6_handle, 1e5)
        ...     print(entry.sequence)  # Print aligned query sequence
    """

    filtered_b6 = defaultdict(list)
    for entry in b6_evalue_filter(b6_handle, e_value, *args, **kwargs):
        filtered_b6[entry.query].append(
            (entry.query_start, entry.query_end, entry._evalue_str))
    fastaq_iter = fasta_iter if fastaq == 'fasta' else fastq_iter
    for fastaqEntry in fastaq_iter(fastaq_handle):
        if fastaqEntry.id in filtered_b6:
            for alignment in filtered_b6[fastaqEntry.id]:
                start = alignment[0] - 1
                end = alignment[1] - 1

                # Get query sequence
                if start < end:
                    query_sequence = fastaqEntry.sequence[start:end]
                elif start > end:
                    query_sequence = fastaqEntry.sequence[end:start][::-1]
                else:
                    query_sequence = fastaqEntry.sequence[start]
                fastaqEntry.sequence = query_sequence

                # Get query quality
                if fastaq == 'fastq':
                    if start < end:
                        query_quality = fastaqEntry.quality[start:end]
                    elif start > end:
                        query_quality = fastaqEntry.quality[end:start][::-1]
                    else:
                        query_quality = fastaqEntry.quality[start]
                    fastaqEntry.quality = query_quality

                # Add E-value to FASTA/Q header
                if fastaqEntry.description == '':
                    fastaqEntry.description = 'E-value: '
                else:
                    fastaqEntry.description += ' E-value: '
                fastaqEntry.description += alignment[2]

                yield fastaqEntry


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--fastaq',
                        type=argparse.FileType('rU'),
                        help='query FASTAQ file')
    parser.add_argument('-b', '--b6',
                        type=argparse.FileType('rU'),
                        help='B6/M8 file with alignment data')
    parser.add_argument('-e', '--e_value',
                        type=float,
                        help='upper E-Value cutoff')
    parser.add_argument('--fastq',
                        action='store_true',
                        help='specifies that input is FASTQ')
    parser.add_argument('-o', '--output',
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
