#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = 'bio_utils',
      version = '0.5.1.0',
      description = 'importable functions often used by bioinformatic scripts',
      classifiers = [
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
      keywords = 'bioinformatics iterators verifiers verify iterate utilities',
      url = 'https://github.com/Brazelton-Lab/bio_utils/',
      download_url = 'https://github.com/Brazelton-Lab/metameta/tarball/'\
                      + '0.5.1.0',
      author = 'Alex Hyer',
      author_email = 'theonehyer@gmail.com',
      license = 'GPL',
      packages = ['bio_utils', 'bio_utils.blast_tools', 'bio_utils.iterators',
                  'bio_utils.verifiers'],
      include_package_data = True,
      zip_safe = False,
      install_requires = [
          'screed'
          ]
      )
