from __future__ import print_function

"""Contains the FileChecker class that provides several file checking methods

FileChecker requires only a single file name as an argument

FileChecker methods follow:
    base:         Same as os.path.basename but without extensions
    ext_present:  Takes a file extension as an argument, determine if the
                  given extension is in the file extensions (below)
    extensions:   Returns all extensions of file as a list
    read_check:   Ensure that the user has permissions to read a file
    write_check:  Ensure that the user has permissions to write a file
    io_check:     Both of the above at the same time
"""

import os
import sys

__version__ = '1.0.0.0'
__author__ = 'Chris Thornton, Alex Hyer'


class FileChecker:

    def __init__(self, file):
        self.file = file

    def base(self):
        """Return base file name w/o extensions"""

        return os.path.basename(self.file).split('.')[0]

    def ext_present(self, ext):
        """Returns True if ext in file extensions, else False"""

        if ext in self.extensions():
            return True
        else:
            return False

    def extensions(self):
        """Return extensions of file as a list"""

        extensions = self.file.split('.')[1:]
        return extensions

    def name(self):
        """Return entire file name"""

        return self.file

    def read_check(self):
        """Ensure that the user has permissions to read a file"""

        if os.access(self.file, os.R_OK):
            return self.file

    def write_check(self):
        """Ensure that the user has permissions to write to a file"""

        if os.access(self.file, os.W_OK):
            return self.file

    def io_check(self):
        """Ensure that the user has permissions to read and write to a file"""

        self.read_check()
        self.write_check()

        return self.file
