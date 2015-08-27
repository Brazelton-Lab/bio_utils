#! /usr/bin/env python

from __future__ import print_function

"""Create MOTHUR group file from one or more FASTA files

Usage:

    group_from_filenames [--seperator] [--position] [Group File] [FASTA Files]

Synopsis:

    Group (sample) names should be in the FASTA file names in a consistent
    format. This script parses the file name by the separator and takes
    the given position as the sample name. A MOTHUR formatted group file is
    written. This is much easier than using MOTHUR to create group files.

Required Arguments:

    Group File:     Name of group file to write
    FASTA Files:    One or more FASTA files to make the group file from

Optional Arguments:

    --separator:    Character to split the file name by [Default: "."]
    --position:     Position after split containing the sample name
                    [Default: 1]

Output:

    A MOTHUR formatted group file.
"""

__version__ = '1.0.0.0'
__author__ = 'Chris Thornton, Alex Hyer'

import argparse
from bio_utils.file_tools.file_check import FileChecker
import os
import sys
import textwrap


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('output', metavar='Group Files',
                        help='Group File to write')
    parser.add_argument('fasta_files', metavar='FASTA Files',
                        nargs='+',
                        help='FASTA files to create group file from')
    parser.add_argument('-s', '--separator', metavar='CHAR',
                        default='.',
                        help='character that separates the sample name from '
                             'the rest of the file name [default "."]')
    parser.add_argument('-p', '--position', metavar='INT',
                        type=int,
                        default=1,
                        help='location of the sample name in the file name '
                             '[default: 1]')
    args = parser.parse_args()

    # Verify user permissions to use files and adjust variables
    fasta_files = [FileChecker(fasta_file) for fasta_file in args.fasta_files]
    for fasta_file in fasta_files:
        fasta_file.read_check()
    out_file = FileChecker(args.output)
    out_file.write_check()
    position = args.position - 1

    with open(out_file.name(), 'w') as out_handle:
        for fasta_file in fasta_files:
            name_parts = os.path.basename(fasta_file.name()) \
                         .split(args.separator)
            if position > len(name_parts):
                print(textwrap.fill('Error: invalid position "{}". There are '
                      'only {} groups created when splitting {} by {}'.format(
                      str(args.position), str(name_parts),
                      os.path.basename(fasta_file.name()), args.separator),
                      79))
                sys.exit(1)
            sample_name = name_parts[position]
            with open(fasta_file.name(), 'rU') as in_handle:
                for line in in_handle:
                    if not line.startswith('>'):
                        continue
                    identifier = line.strip('>\n').split()[0]
                    if ':' in identifier:
                        identifier = identifier.replace(':', '_')
                    out_handle.write('{}\t{}\n'.format(identifier,
                                                       sample_name))

if __name__ == '__main__':
    main()
    sys.exit(0)
