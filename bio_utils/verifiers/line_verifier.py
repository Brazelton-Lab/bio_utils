#!/usr/bin/env python
from __future__ import print_function

'''General function for analyzing lines against a regex'''

__version__ = '1.0.1.0'

import codecs
try:
    from metameta_utils.output import output
except:
    pass
import re
import sys

def verify_lines(lines, regex, delimiter, log_file = None):
    '''checks each line against regex for validity

    If a line does not match the regex, the line and regex
    are broken down by the delimiter and each segmetn is analyzed
    to produce and accurate error message.
    '''
    
    cRegex = re.compile(regex)
    splitRegex = regex.split(delimiter)
    pythonType = int(sys.version.split('.')[0])
    decoder = 'unicode-escape' if pythonType == 3 else 'string-escape'
    dedelimitr = codecs.decode(delimiter, decoder)
    for line in lines:
        match = re.match(cRegex, line)
        if not match:
            splitLine = line.split(dedelimiter)
            for regexSegment, lineSegment in zip(splitRegex, splitLine):
                if not regexSegment.startswith('^'):
                    regexSegment = '^' + regexSegment
                if not regexSegment.endswith('$'):
                    regexSegment += '$'
                matchSegment = re.match(regexSegment, lineSegment)
                if not matchSegment:
                    message = 'The following line segment:\n\n{}\n\n'\
                              + 'Does not match the regular expression:\n'\
                              + '\n{}\n\nSee https://docs.python.org/3.4/'\
                              + 'library/re.html for information '\
                              + 'on how to interpret regular expression.\n'\
                              + 'The entire entry containing the error '\
                              + 'follows:\n\n{}\n'.format(lineSegment,
                                                          regexSegment, line)
                    try:
                        output(message, 1, 1, log_file = log_file)
                    except:
                        print(message)
                    return False
    return True
