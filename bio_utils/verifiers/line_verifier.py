#!/usr/bin/env python

from __future__ import print_function

"""General function for analyzing lines against a regex

Copyright:

    line_verifier.py compare lines of file to regex to determine validity
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

import codecs
import re
import sys

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '1.0.5'


def verify_lines(lines, regex, delimiter):
    """checks each line against regex for validity

    If a line does not match the regex, the line and regex
    are broken down by the delimiter and each segment is analyzed
    to produce and accurate error message.

    :param lines: list of entries to check regex against
    :type lines: list

    :param regex: regex to match entries in lines against
    :type regex: str

    :param delimiter: delimiter of entry and to subdivide by if mismatch
    :type delimiter: str

    :return: True if all lines match regex, else False
    :rtype: boolean
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
                                                          regex_segment,
                                                          line)
                    print(message)
                    return False
    return True
