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
__version__ = '1.0.3'


def blast_to_cigar(query_seq, match_seq, subject_seq, cigar_age='old'):
    """converts BLAST alignment into a old or new CIGAR line

    :param query_seq: The aligned query sequence
    :type query_seq: str

    :param match_seq: The sequence visually depicting the alignment
    :type match_seq: str

    :param subject_seq: The aligned subject sequence
    :type subject_seq: str

    :param cigar_age: 'old' or 'new'. Whether or not to use the old version
                      of Cigar containing only 'M' for matches and mismatches
                      or to give more detail on the alignment (old vs. new)
    :type cigar_age: str

    :returns: Cigar line of BLAST alignment
    :rtype: str
    """

    # Translate XML alignment to CIGAR characters
    cigar_line_raw = []
    for query, match, subject in zip(query_seq, match_seq, subject_seq):
        if query == '-':
            cigar_line_raw.append('D')
            continue
        elif subject == '-':
            cigar_line_raw.append('I')
            continue
        elif match == '+' or match == '|' or match.isalpha():
            if match != '+' and cigar_age == 'new':
                cigar_line_raw.append('=')
                continue
            elif match == '+' and cigar_age == 'new':
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
        if letter[0] == cigar_len:
            if repeats != 1:
                cigar_line.append(str(repeats))
                repeats = 1
            cigar_line.append(letter[1])
        last_position = letter[1]

    return ''.join(cigar_line)
