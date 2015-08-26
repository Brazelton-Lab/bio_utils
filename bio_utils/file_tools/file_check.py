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


class IOChecker:

    def __init__(self, file):
        self.file = file

    def name(self):
        """Return file name"""

        return self.file

    def read_check(self):
        """Ensure that the user has permissions to read a file"""

        try:
            test_handle = open(self.file, 'rU')
        except IOError as error:
            print('You do no have permission to read {0}'.format(self.file))
            print(error)
            sys.exit(1)
        else:
            test_handle.close()
        return self.file

    def write_check(self):
        """Ensure that the user has permissions to write to a file"""

        try:
            test_handle = open(self.file, 'a')
        except IOError as error:
            print('You do no have permission to write {0}'.format(self.file))
            print(error)
            sys.exit(1)
        else:
            test_handle.close()
        return self.file

    def io_check(self):
        """Ensure that the user has permissions to read and write to a file"""

        self.read_check()
        self.write_check()

        return self.file
