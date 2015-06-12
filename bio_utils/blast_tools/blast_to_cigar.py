#!/usr/bin/srv python

'''Translates a BLAST XML alignment into a CIGAR line'''

__version__ = '1.0.0.0'

def blast_to_cigar(querySeq, matchSeq, subjectSeq, cigar_age = 'old'):
    '''converts BLAST alignment into a old or new CIGAR line'''

    cigarLineRaw = []
    for query, match, subject in zip(querySeq, matchSeq, subjectSeq):
        if query == '-':
            cigarLineRaw.append('D')
            continue
        elif subject == '-':
            cigarLineRaw.append('I')
            continue
        elif match == '+' or match == '|' or match.isalpha():
            if match != '+' and cigar_age == 'new':
                cigarLineRaw.append('=')
                continue
            elif match == '+' and cigar_age == 'new':
                cigarLineRaw.append('X')
                continue
            else:
                cigarLineRaw.append('M')
                continue
        elif cigar_age == 'new':
            cigarLineRaw.append('X')
            continue
        else:
            cigarLineRaw.append('M')
    cigarLine = []
    lastPosition = ''
    repeats = 1
    cigarLen = len(cigarLineRaw)
    for letter in enumerate(cigarLineRaw):
        if letter[1] == lastPosition:
            repeats += 1
        else:
            if repeats != 1:
                cigarLine.append(str(repeats))
                repeats = 1
            cigarLine.append(lastPosition)
        if letter[0] == cigarLen:
            if repeats != 1:
                cigarLine.append(str(repeats))
                repeats = 1
            cigarLine.append(letter[1])
        lastPosition = letter[1]
    return ''.join(cigarLine)
