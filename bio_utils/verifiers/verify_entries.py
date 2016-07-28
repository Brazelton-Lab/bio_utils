#! /usr/bin/env python

"""General function for analyzing entries against a regex

Copyright:

    verify_entries.py compare lines of file to regex to determine validity
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
__version__ = '2.0.1'

class FormatError(Exception):
    """Exception to store errors when bad format found

    Attributes:
        template (str): Template of format that subject failed to match

        subject (str): String of failed format

        part (int): Index of template and subject if given regex and subject
            are subsets of a larger template and subject

        message (str): Error message

    Examples:
        Note: These doctests may not pass, examples are only in doctest
        format as per convention. bio_utils uses pytests for testing.

        >>> import re
        >>> regex = r'^>.+\\n[ACGTU]+\\n$'
        >>> subject = r'>entry1\\nAGGGACTZZHZHJA\\n'
        >>> if not re.match(regex, subject):
        ...     raise FormatError(template=regex,
        ...                       subject=subject,
        ...                       message='Error with format')
        Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
            File "bio_utils/verifiers/verify_entires.py", line 59, in FormatError
                raise FormatError(message=msg)
        bio_utils.verifiers.verify_entries.FormatError: Error with format!
    """

    def __init__(self, template=None, subject=None, part=None, message=None):
        self.template = template
        self.subject = subject
        self.part = part
        self.message = message

        # Only print error if message given so that errors can be used to
        # convey data on error for intelligent handling downstream
        if message:
            super(Exception, self).__init__(message)


def entry_verifier(entries, regex, delimiter):
    """Checks each entry against regex for validity,

    If an entry does not match the regex, the entry and regex
    are broken down by the delimiter and each segment is analyzed
    to produce an accurate error message.

    Args:
        entries (list): List of entries to check with regex

        regex (str): Regular expression to compare entries with

        delimiter (str): Character to split entry and regex by, used to check
            parts of entry and regex to narrow in on the error

    Raises:
        FormatError: Class containing regex match error data

    Example:
        >>> regex = r'^>.+\\n[ACGTU]+\\n$'
        >>> entry = [r'>entry1\\nAGGGACTA\\n']
        >>> entry_verifier(entry, regex, '\\n')
    """

    cregex = re.compile(regex)  # Compiling saves time if many entries given

    # Encode raw delimiter in order to split a bad entry
    python_version = int(sys.version.split('.')[0])
    decoder = 'unicode-escape' if python_version == 3 else 'string-escape'
    dedelimiter = codecs.decode(delimiter, decoder)

    for entry in entries:
        match = re.match(cregex, entry)

        # Match failed, check regex and entry parts for error
        if not match:
            split_regex = regex.split(delimiter)
            split_entry = entry.split(dedelimiter)
            part = 0  # "Enumerate" zipped iter
            for regex_segment, entry_segment in zip(split_regex, split_entry):
                # Ensure regex_segment only matches entire entry_segment
                if not regex_segment[0] == '^':
                    regex_segment = '^' + regex_segment
                if not regex_segment[-1] == '$':
                    regex_segment += '$'

                # If segment fails, raise error and store info on failure
                if not re.match(regex_segment, entry_segment):
                    raise FormatError(template=regex_segment,
                                      subject=entry_segment,
                                      part=part)

                part += 1  # Increase enumeration
