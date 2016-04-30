#!/usr/bin/srv python

"""Returns subject sequence from BLAST hits below a specified e-value

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
from collections import defaultdict
from bio_utils.iterators import fasta_iter
import sys

__author__ = 'William Brazelton, Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.1.6'


def subject_sequence_retriever(fasta_handle, b6_handle, e_value):
    """Returns FASTA entries for subject sequences from BLAST hits

    Stores B6/M8 entries with e-values below the e_value cutoff. Then iterates
    through the FASTA file and if an entry matches the subject of an B6/M8
    entry, it's sequence is extracted and returned as a FASTA entry
    plus the e-value.

    :param fastaq_handle: FASTAfile handle
    :type fastaq_handle: File Object

    :param b6_handle: B6/M8 file handle
    :type b6_handle: File Object

    :param e_value: Max evalue to be returned
    :type e_value: float

    :return: FastaEntry class
    :rtype: FastaEntry
    """

    filtered_b6 = defaultdict(list)
    for entry in b6_iter(b6_handle):
        if float(entry.evalue) <= e_value:
            filtered_b6[entry.subject].append(
                (int(entry.subject_start), int(entry.subject_end),
                 float(entry.evalue)))
    for fastaEntry in fasta_iter(fasta_handle):
        if fastaEntry.name in filtered_b6:
            for pair in filtered_b6[fastaEntry.name]:
                start = pair[0] - 1
                end = pair[1] - 1
                if start < end:
                    subject_sequence = fastaEntry.sequence[start:end]
                elif start > end:
                    subject_sequence = fastaEntry.sequence[end:start][::-1]
                else:
                    subject_sequence = fastaEntry.sequence[start]
                fastaEntry.sequence = subject_sequence
                fastaEntry.description += str(pair[2])
                yield fastaEntry


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('fastaFile',
                        help='subject FASTA file')
    parser.add_argument('b6File',
                        help='B6/M8 file with alignment data')
    parser.add_argument('e_value',
                        help='upper e-value cutoff')
    parser.add_argument('output',
                        default=None,
                        nargs='?',
                        help=' optional output file, defaults to STDOUT')
    args = parser.parse_args()

    with open(args.fastaFile, 'rU') as fasta_handle:
        with open(args.b6File, 'rU') as b6_handle:
            for fastaEntry in subject_sequence_retriever(fasta_handle,
                                                         b6_handle,
                                                         float(args.e_value)):
                if args.output is not None:
                    with open(args.output, 'a') as out_handle:
                        out_handle.write(fastaEntry.write())
                else:
                    print(fastaEntry.write())


if __name__ == '__main__':
    main()
    sys.exit(0)
