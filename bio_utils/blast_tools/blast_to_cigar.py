#!/usr/bin/srv python

"""Translates a BLAST XML alignment into a CIGAR line"""

__version__ = '1.0.1.1'
__author__ = 'Alex Hyer'


def blast_to_cigar(query_seq, match_seq, subject_seq, cigar_age='old'):
    """converts BLAST alignment into a old or new CIGAR line"""

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
