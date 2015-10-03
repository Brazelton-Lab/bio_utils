#!/usr/bin/env python

from setuptools import setup

setup(name='bio_utils',
      version='0.7.3.0',
      description='importable functions often used by bioinformatic scripts',
      classifiers=[
          'Development Status :: 6 - Mature',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      keywords='bioinformatics iterators verifiers verify iterate utilities',
      url='https://github.com/Brazelton-Lab/bio_utils/',
      download_url='https://github.com/Brazelton-Lab/metameta/tarball/' \
                   + '0.7.3.0',
      author='Alex Hyer',
      author_email='theonehyer@gmail.com',
      license='GPL',
      packages=['bio_utils',
                'bio_utils.blast_tools',
                'bio_utils.iterators',
                'bio_utils.verifiers',
                'bio_utils.mothur_tools',
                'bio_utils.file_tools'
                ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'screed'
      ],
      entry_points={
          'console_scripts': [
              'binary_verifier = bio_utils.verifiers.binary:main',
              'fasta_verifier = bio_utils.verifiers.fasta:main',
              'fastq_verifier = bio_utils.verifiers.fastq:main',
              'fastr_verifier = bio_utils.verifiers.fastr:main',
              'gff3_verifier = bio_utils.verifiers.gff3:main',
              'm8_verifier = bio_utils.verifiers.m8:main',
              'sam_verifier = bio_utils.verifiers.sam:main',
              'filter_m8_evalue = bio_utils.blast_tools.filter_m8_evalue:main',
              'retrieve_query_sequences = bio_utils.blast_tools.'
                  'retrieve_query_sequences:main',
              'retrieve_subject_sequences = bio_utils.blast_tools.'
                  'retrieve_subject_sequences:main',
              'modify_tax_summary = bio_utils.mothur_tools.'
                  'modify_tax_summary:main',
              'convert_count_to_shared = bio_utils.mothur_tools.'
                  'convert_count_to_shared:main'
          ]
      }
      )
