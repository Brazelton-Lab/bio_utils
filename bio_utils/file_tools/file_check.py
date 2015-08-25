from __future__ import print_function

"""Library of file-checking functions

This library contains three file checking functions:
    read_check:   Ensure that the user has permissions to read a file
    write_check:  Ensure that the user has permissions to write a file
    io_check:   Both of the above at the same time
"""

import sys

__version__ = '0.0.0.1'
__author__ = 'Chris Thornton, Alex Hyer'


def read_check(file):
    """Ensure that the user has permissions to read a file"""

    try:
        test_handle = open(file, 'rU')
    except IOError as error:
        print('You do no have permission to read {0}'.format(file))
        print(error)
        sys.exit(1)
    else:
        test_handle.close()
    return file


def write_check(file):
    """Ensure that the user has permissions to write to a file"""

    try:
        test_handle = open(file, 'a')
    except IOError as error:
        print('You do no have permission to write to {0}'.format(file))
        print(error)
        sys.exit(1)
    else:
        test_handle.close()
    return file


def io_check(file):
    """Ensure that the user has permissions to read and write to a file"""

    read_check(file)
    write_check(file)

    return file
