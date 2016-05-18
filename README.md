bio_utils
==========

Python package containing modules of commonly used bioinformatic scripts

Last Stable Version: 0.7.13

Current Version: 0.7.14a1

IMPORTANT NOTE
--------------

bio_utils will be undergoing massive changes soon

Purpose
-------

bio_utils provides a series of scripts accomplishing tedious steps often
used by larger bioinformatic programs. These scripts are designed in a generic
and flexible manner so that most if not all scripts utilizing bio_utils
can do so with little to no modification of bio_utils itself. To accomplish
this task, all scripts are importable Python library modules and accomplish
only one generic task each.

Bugs
=====

There are currently no known bugs in bio_utils. Please email Alex Hyer at
theonehyer@gmail.com with bugs and typos.

Requirements
============

Python 2.7+ or 3.4+

Installation
============

pip install bio_utils

Scripts
========

bio_utils contains several sub-packages containing scripts of similar function.
All scripts are written such that their functionality is importable
(i.e. the packages serve as Python libraries) but many scripts can also be run
independently. Any such script is linked to /usr/local/bin/
(Unix-like systems). Each sub-package and it's scripts are described below:

blast_tools
-----------

blast_tools contains a variety of scripts to assist with filtering and using
BLAST data. All scripts except blast_to_cigar are also stand-alone programs
and executable as "[script name]".

Scripts:
* blast_to_cigar: convert BLAST+ XML alignment lines to a CIGAR line
* filter_b6_evalue: filters a M8 (BLAST+ output format 6) file by e-value
* retrieve_query_sequences: recover query FASTA sequences for BLAST hits below
                            a given e-value
* retrieve_subject_sequences: recover subject FASTA sequences for BLAST hits
                              below a given e-value

iterators
---------

iterators simply contains a number of file iterators for reading, parsing, and
returning lines of a file as dictionaries. screed is used for reading
FASTQ files. See individual scripts for dictionary structure.

Import as "from bio_utils.iterators import [script]_iter"

Scripts:
* b6: reads, parses, and returns lines of a M8 file (BLAST+ output format 6)
      Attributes: query, subject, perc_identical, align_len,
      mismatchs, gaps, query_start, query_end, subject_start, subject_end,
      evalue, bit_score
* fasta: reads, parses, and returns lines of a FASTA file
         Attributes: name, description, sequence
* fastq: reads, parses, and returns lines of a FASTQ file
         Attributes: name, description, sequence, quality
* gff3: reads, parses, and returns lines of a GFF3 file
        Attributes: seqid, source, type, start, end, score,
        strand, phase, attributes (Note: if 'prokka=True' is given,
        dynamic parsing of attributes as per the GFF3 file of PROKAA 1.12-beta
        is performed)
* sam: reads, parses, and returns lines of a SAM file
       Attributes: qname, flag, rname, pos, mapq, cigar, rnext,
       pnext, tlen, seq, qual

verifiers
---------

verifiers contains scripts that examine a file type to ensure that the file is
formatted correctly. Each script returns True if the file is formatted
correctly and False if the file is incorrectly formatted. If the file is
incorrectly formatted, a description of the formatting error is printed. All
scripts in verifiers are also stand-alone programs and executable
 as "[script name]_verifier".
 
 Import as "from bio_utils.verifiers import [script]_verifier"

Scripts:
* b6: verifies a M8 file (BLAST+ output format 6)
* binary: guesses whether or not a file is binary
* fasta: verifies a FASTA file
* fastq: verifies a FASTQ file
* gff3: verifies a GFF3 file
* sam: verifies a SAM file

Contributors
============

Alex Hyer (theonehyer@gmail.com)

Chris Thornton (christopher.thornton@utah.edu)

William Brazelton