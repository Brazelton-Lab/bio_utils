#! /usr/bin/env python

"""Translates a BLAST XML alignment into a CIGAR line

Copyright:

    blast_to_cigar.py convert BLAST XML alignments into CIGAR lines
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

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '2.0.1'


def blast_to_cigar(query_seq, match_seq, subject_seq, cigar_age='new'):
    """converts BLAST alignment into a old or new CIGAR line

    Args:
        query_seq (str): Aligned portion of query sequence

        match_seq (str): Alignment sequence

        subject_seq (str): Aligned portion of subject/reference sequence

        cigar_age (str): ['old', 'new'] CIGAR format to use, new is highly
            detailed while old is fairly minimalistic

    Returns:
        str: CIGAR string

    Raises:
        ValueError: If query_seq, match_seq, and match_seq not same length

    Examples:
        >>> query = 'AAGGG--CCTTGTA'
        >>> subject = 'AAGCCTTCCAGGTA'
        >>> alignment_old = '|||||  |||||||'
        >>> alignment_new = 'AAG++  CC++GTA'
        >>> blast_to_cigar(query, alignment_new, subject)
        3=2X2D2=2X3=
        >>> blast_to_cigar(query, alignment_old, subject, cigar_age='old')
        5M2D7M
    """

    if not len(query_seq) == len(match_seq) \
            or not len(query_seq) == len(subject_seq) \
            or not len(subject_seq) == len(match_seq):
        raise ValueError('query_seq, match_seq, and subject_seq not same '
                         'lengths.')

    # Translate XML alignment to CIGAR characters
    cigar_line_raw = []
    for query, match, subject in zip(query_seq, match_seq, subject_seq):
        if query == '-':  # Deletion
            cigar_line_raw.append('D')
            continue
        elif subject == '-':  # Insertion
            cigar_line_raw.append('I')
            continue
        elif match == '+' or match == '|' or match.isalpha():  # Match
            if match != '+' and cigar_age == 'new':  # Positive match
                cigar_line_raw.append('=')
                continue
            elif match == '+' and cigar_age == 'new':  # Mismatch
                cigar_line_raw.append('X')
                continue
            else:
                cigar_line_raw.append('M')
                continue
        elif cigar_age == 'new':
            cigar_line_raw.append('X')
            continue
        else:
            cigar_line_raw.append('M')

    # Replace repeat characters with numbers
    cigar_line = []
    last_position = ''
    repeats = 1
    cigar_len = len(cigar_line_raw)
    for letter in enumerate(cigar_line_raw):
        if letter[1] == last_position:
            repeats += 1
        else:
            if repeats != 1:
                cigar_line.append(str(repeats))
                repeats = 1
            cigar_line.append(last_position)
        if letter[0] == cigar_len - 1:
            if repeats != 1:
                cigar_line.append(str(repeats))
                repeats = 1
            cigar_line.append(letter[1])
        last_position = letter[1]

    return ''.join(cigar_line)
