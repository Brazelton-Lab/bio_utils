#!/usr/bin/env python

from __future__ import print_function

"""Includes fully phylogeny in Mothur taxonomy summary files

Usage:

    modify_tax_summary [--tax_levels] taxonomy_summary_file

Synopsis:

    Adds full phylogeny in taxon field of Mothur taxonomy summary file and
    outputs additional files at different taxonomic levels.

Required Arguments:

    taxonomy_summary_file:  Mothur generated taxonomy summary file

Optional Arguments:

    --tax_levels    List which taxonomic ranks to create separate files for.
                    This needs to be a comma separated list containing
                    only values from the following list:
                        domain
                        phylum
                        class
                        order
                        family
                        genus
                        species
                        strain

Output:

    The primary output file is a '.mod' file which is the MOTHUR taxonomy
    summary file with the full phylogeny in the taxon field. Additionally,
    for each taxon rank specified, a '.[tax_level]' file is created which
    is essentially the '.mod' file but only includes entries at the given
    taxonomic level.
"""

import argparse
from bio_utils.file_tools.file_check import FileChecker
import os
import sys
import textwrap

__version__ = '1.1.1.0'
__author__ = 'Chris Thornton, Alex Hyer'


def parse_tax_file(tax_file):
    """Parses a Mothur generated taxonomy summary file into a dictionary"""

    taxonomy = {}
    with open(tax_file, 'rU') as tax_handle:
        header = tax_handle.readline().strip().replace(' ', '').split('\t')
        index_map = {}
        for index, col_header in enumerate(header):
            index_map[col_header] = index
        try:
            rank_index = index_map['rankID']
            taxon_index = index_map['taxon']
            level_index = index_map['taxlevel']
        except KeyError:
            print('Error: Cannot parse header')
            print(textwrap.fill('Error: Please verify that the header is '
                                'formatted correctly in the taxonomy summary '
                                'file', 79))
            sys.exit(1)
        col_order = [level_index, rank_index, taxon_index]
        sample_info = [header[i] for i in range(len(header))
                       if i not in col_order]
        new_header = '\t'.join([header[i] for i in col_order] + sample_info)

        for line in tax_handle:
            split_line = line.strip().replace(' ', '').split('\t')
            rank_id = split_line[rank_index]
            taxon = split_line[taxon_index]
            rank_level = split_line[level_index]
            data = [split_line[i] for i in range(len(split_line))
                    if i not in col_order]
            taxonomy[rank_id] = {
                'taxon': taxon, 'level': rank_level,
                'data': data
                }
    return new_header, taxonomy


def split_args(arguments):
    """Further split arguments and checks them"""

    choices = [
        'domain',
        'phylum',
        'class',
        'order',
        'family',
        'genus',
        'species',
        'strain'
    ]
    arguments = [i.lstrip() for i in arguments.split(',')]
    for argument in arguments:
        if argument not in choices:
            print('Error: {0} not in {1}\n'.format(
                argument, '\n'.join(arguments)
            ))
            sys.exit(1)
    return arguments


def write_output(taxonomy, taxon, out_handle):
    """Write properly formatted Mothur taxonomy output"""

    output = taxonomy[taxon]['level'] + '\t' + taxon + '\t' + \
             taxonomy[taxon]['phylogeny'] + '\t' + \
             '\t'.join(taxonomy[taxon]['data']) + '\n'
    out_handle.write(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('tax_file', metavar='taxonomy summary file',
                        help='Mothur generated taxonomy summary file')
    parser.add_argument('-l', '--tax_levels', metavar='Rank', dest='rank',
                        default='family,genus',
                        help='Space separated list of ranks for output files')
    args = parser.parse_args()

    FileChecker(args.tax_file).read_check()
    args.rank = split_args(args.rank)
    tax_levels = {
        'domain': 1,
        'phylum': 2,
        'class': 3,
        'order': 4,
        'family': 5,
        'genus': 6,
        'species': 7,
        'strain': 8
    }
    tax_file = os.path.basename(args.tax_file)
    out_file = FileChecker(tax_file + '.mod')
    out_file.write_check()
    tax_files = [('{0}.{1}'.format(tax_file, rank), tax_levels[rank])
                 for rank in args.rank]
    header, taxonomy = parse_tax_file(args.tax_file)

    # edit taxon name to include full taxonomic classifications
    with open(out_file.name(), 'w') as out_handle:
        out_handle.write(header + '\n')
        for taxon in sorted(taxonomy):
            phylogeny = None
            phylogeny_rank = []
            split_rank = taxon.split('.')
            for index in range(len(split_rank)):
                clade = '.'.join(split_rank[0:index + 1])
                phylogeny_rank.append(clade)
            phylogeny = ';'.join([taxonomy[i]['taxon']
                                  for i in phylogeny_rank if i != '0'])
            if phylogeny:
                taxonomy[taxon]['phylogeny'] = phylogeny
            else:
                taxonomy[taxon]['phylogeny'] = taxonomy[taxon]['taxon']
            write_output(taxonomy, taxon, out_handle)

    # write outfiles for given (or default) levels
    for tax_file in tax_files:
        out_name = FileChecker(tax_file[0])
        out_name.write_check()
        rank = tax_file[1]
        tax_subset = [taxon for taxon in taxonomy
                      if (len(taxon.split('.')) - 1) == rank]
        with open(out_name.name(), 'w') as out_handle:
            out_handle.write(header + '\n')
            for taxon in sorted(tax_subset):
                write_output(taxonomy, taxon, out_handle)


if __name__ == '__main__':
    main()
    sys.exit(0)
