bio_utils
==========

Python package containing modules of commonly used bioinformatic scripts

purpose
-------

    bio_utils provides a series of scripts accomplishing tedious steps often used by larger bioinformatic programs.
These scripts are designed in a generic and flexible manner so that most if not all scripts utilizing bio_utils
can do so with little to no modification of bio_utils itself. To accomplish this task, all scripts are importable
Python library modules and accomplish only one generic task each.

Bugs
=====

There are currently no known bugs in bio_utils. Please email Alex Hyer at theonehyer@gmail.com with bugs and typos.

Requirements
============

Python 2.7+ or 3.4+

Python Libraries:

* screed

Installation
============

pip install bio_utils

Scripts
========

bio_utils contains several sub-packages containing scripts of similar function.
Each sub-package and it's scripts are described below:

iterators
---------

iterators simply contains a number of file iterators for reading, parsing, and returning lines of a file as dictionaries.
screed is used for reading FASTA and FASTQ files. See individual scripts for dictionary structure.

Scripts:
* fastr: reads, parses, and returns lines of a FASTR file {'name':, 'description':, 'sequence':}
* gff3: reads, parses, and returns lines of a GFF3 file {'seqid':, 'source':, 'type':, 'start':, 'end':, 'score':, 'strand':, 'phase':, 'attributes':}
* m8: reads, parses, and returns lines of a M8 file {'queryID':, 'subjectID':, 'percIdentical':, 'alignLen':, 'mismatchCount':, 'gapCount':, 'queryStart':, 'queryEnd':, 'subjectStart':, 'subjectEnd':, 'eValue':, 'bitScore':}
* sam: reads, parses, and returns lines of a SAM file {'qname':, 'flag':, 'rname':, 'pos':, 'mapq':, 'cigar':, 'rnext':, 'pnext':, 'tlen':, 'seq':, 'qual':}

verifiers
---------

verifiers contains scripts that examine a file type to ensure that the file is formatted correctly.
Returns True if the file is formatted correctly and False if the file is incorrectly formatted.
If the file is incorrectly formatted, a description of what the error is and where the error is.

Scripts:
* binary: guesses whether or not a file is binary
* fasta: verifies a FASTA file
* fastq: verifies a FASTQ file
* fastr: verifies a FASTR file
* gff3: verifies a GFF3 file
* m8: verifies a M8 file
* sam: verifies a SAM file

blast_tools
-----------

blast_tools contains a variety of scripts to assist with filtering and using BLAST data.
All scripts except blast_to_cigar are also stand-alone programs.

Scripts:
* blast_to_cigar: convert BLAST+ XML alignment lines to a CIGAR line
* m8_evalue_filter: filters a M8 file by e-value
* subject_sequence_filter: recover subject FASTA sequences for BLAST hits below a given e-value

Contributors
============

Alex Hyer (theonehyer@gmail.com)

Chris Thornton