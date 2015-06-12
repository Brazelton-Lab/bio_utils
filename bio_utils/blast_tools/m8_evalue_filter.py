#!/usr/bin/srv python

'''Returns only those lines of an M8 file below a specified e-value

Usage:

    m8_evalue_filter.py <m8File> <e_value> <output>

Prints or writes lines of M8 value under maximum e-value cutoff
'''

import argparse
from bio_utils.iterators.m8 import m8_iter
import sys

__version__ = '1.0.0.0'

def m8_evalue_filter(handle, e_value):
    '''Returns lines from handle with e-value below or equal to e_value'''

    for m8Entry in m8_iter(handle):
        if float(m8Entry['eValue']) <= e_value:
            yield m8Entry

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
                                     formatter_class = argparse.\
                                     RawDescriptionHelpFormatter)
    parser.add_argument('m8File',
                        help = 'M8 file with alignment data')
    parser.add_argument('e_value',
                        help = 'upper e-value cutoff')
    parser.add_argument('output',
                        default = None,
                        nargs = '?',
                        help = ' optional output file, defaults to STDOUT')
    args = parser.parse_args()

    with open(args.m8File, 'rU') as m8_handle:
        for m8Entry in m8_evalue_filter(m8_handle, args.e_value):
            entry = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'\
                    .format(m8Entry['queryID'], m8Entry['subjectID'],\
                            m8Entry['percIdentical'], m8Entry['alignLen'],\
                            m8Entry['mismatchCount'], m8Entry['gapCount'],\
                            m8Entry['queryStart'], m8Entry['queryEnd'],\
                            m8Entry['subjectStart'], m8Entry['subjectEnd'],\
                            m8Entry['eValue'], m8Entry['bitScore'])
            if args.output != None:
                with open(args.output, 'w') as out_handle:
                    out_handle.write(entry)
            else:
                print(entry)
    sys.exit(0)
