#! /usr/bin/env python

"""Setup file to build and install bio_utils PyPI package

Copyright:

    setup.py build and install bio_utils PyPI package
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

from setuptools import setup

setup(name='bio_utils',
      version='0.7.14a1',
      description='importable functions often used by bioinformatic scripts',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      keywords='bioinformatics iterators verifiers verify iterate utilities',
      url='https://github.com/Brazelton-Lab/bio_utils/',
      download_url='https://github.com/Brazelton-Lab/metameta/tarball/'
                   '0.7.14a1',
      author='Alex Hyer',
      author_email='theonehyer@gmail.com',
      license='GPLv3',
      packages=['bio_utils',
                'bio_utils.blast_tools',
                'bio_utils.iterators',
                'bio_utils.verifiers'
                ],
      include_package_data=True,
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'binary_verifier = bio_utils.verifiers.binary:main',
              'fasta_verifier = bio_utils.verifiers.fasta:main',
              'fastq_verifier = bio_utils.verifiers.fastq:main',
              'gff3_verifier = bio_utils.verifiers.gff3:main',
              'b6_verifier = bio_utils.verifiers.b6:main',
              'sam_verifier = bio_utils.verifiers.sam:main',
              'filter_b6_evalue = bio_utils.blast_tools.filter_b6_evalue:main',
              'retrieve_query_sequences = bio_utils.blast_tools.'
                  'retrieve_query_sequences:main',
              'retrieve_subject_sequences = bio_utils.blast_tools.'
                  'retrieve_subject_sequences:main',
          ]
      }
      )
