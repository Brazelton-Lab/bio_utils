#!/usr/bin/srv python

"""Returns subject sequence from BLAST hits below a specified e-value

Usage:

    retrieve_subject_sequences.py --fastqq <FASTA file>
                                  --b6 <B6 or M8 file> --e_value <max E-Value>
                                  --output <output file>

Copyright:

    retrieve_subject_sequences.py recover subject sequences of BLAST alignment
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
from bio_utils.iterators import fasta_iter
from collections import defaultdict
import sys

__author__ = 'William Brazelton, Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.2.1'


def subject_sequence_retriever(fasta_handle, b6_handle, e_value):
    """Returns FASTA entries for subject sequences from BLAST hits

    Stores B6/M8 entries with E-Values below the e_value cutoff. Then iterates
    through the FASTA file and if an entry matches the subject of an B6/M8
    entry, it's sequence is extracted and returned as a FASTA entry
    plus the E-Value.

    Args:
        fasta_handle (file): FASTA file handle, can technically
            be any iterable that returns FASTA "lines"

        b6_handle (file): B6/M8 file handle, can technically
            be any iterable that returns B6/M8 "lines"

        e_value (float): Max E-Value of entry to return

    Yields:
        FastaEntry: class containing all FASTA data

    Example:
        Note: These doctests will not pass, examples are only in doctest
        format as per convention. bio_utils uses pytests for testing.

        >>> fasta_handle = open('test.fasta')
        >>> b6_handle = open('test.b6')
        >>> for entry in subject_sequence_retriever(fasta_handle,
        ...                                       b6_handle, 1e5)
        ...     print(entry.sequence)  # Print aligned subject sequence
    """

    filtered_b6 = defaultdict(list)
    for entry in b6_iter(b6_handle):
        if entry.evalue <= e_value:
            filtered_b6[entry.subject].append(
                (entry.subject_start, entry.subject_end, entry.evalue))
    for fastaEntry in fasta_iter(fasta_handle):
        if fastaEntry.name in filtered_b6:
            for alignment in filtered_b6[fastaEntry.name]:
                start = alignment[0] - 1
                end = alignment[1] - 1
                if start < end:
                    subject_sequence = fastaEntry.sequence[start:end]
                elif start > end:
                    subject_sequence = fastaEntry.sequence[end:start][::-1]
                else:
                    subject_sequence = fastaEntry.sequence[start]
                fastaEntry.sequence = subject_sequence
                fastaEntry.description += ' E-Value: '
                fastaEntry.description += str(alignment[2])
                yield fastaEntry


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--fasta',
                        type=argparse.FileType('rU'),
                        help='subject FASTA file')
    parser.add_argument('-b', '--b6',
                        type=argparse.FileType('rU'),
                        help='B6/M8 file with alignment data')
    parser.add_argument('-e', '--e_value',
                        type=float,
                        help='upper e-value cutoff')
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        nargs='?',
                        help=' optional output file, defaults to STDOUT')
    args = parser.parse_args()

    for fastaEntry in subject_sequence_retriever(args.fasta,
                                                 args.b6,
                                                 args.e_value):
        args.out.write(fastaEntry.write())


if __name__ == '__main__':
    main()
    sys.exit(0)
