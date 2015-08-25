#!/usr/bin/env python

from __future__ import print_function

"""General function for analyzing lines against a regex"""

__version__ = '1.0.3.1'
__author__ = 'Alex Hyer'

import codecs
import re
import sys


def verify_lines(lines, regex, delimiter):
    """checks each line against regex for validity

    If a line does not match the regex, the line and regex
    are broken down by the delimiter and each segmetn is analyzed
    to produce and accurate error message.
    """

    cregex = re.compile(regex)
    split_regex = regex.split(delimiter)
    python_type = int(sys.version.split('.')[0])
    decoder = 'unicode-escape' if python_type == 3 else 'string-escape'
    dedelimiter = codecs.decode(delimiter, decoder)
    for line in lines:
        match = re.match(cregex, line)
        if not match:
            split_line = line.split(dedelimiter)
            for regex_segment, lineSegment in zip(split_regex, split_line):
                if not regex_segment.startswith('^'):
                    regex_segment = '^' + regex_segment
                if not regex_segment.endswith('$'):
                    regex_segment += '$'
                match_segment = re.match(regex_segment, lineSegment)
                if not match_segment:
                    message = 'The following line segment:\n\n{}\n\n' \
                              + 'Does not match the regular expression:\n' \
                              + '\n{}\n\nSee https://docs.python.org/3.4/' \
                              + 'library/re.html for information ' \
                              + 'on how to interpret regular expression.\n' \
                              + 'The entire entry containing the error ' \
                              + 'follows:\n\n{}\n'.format(lineSegment,
                                                          regex_segment, line)
                    print(message)
                    return False
    return True
