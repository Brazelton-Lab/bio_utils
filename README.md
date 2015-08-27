bio_utils
==========

Python package containing modules of commonly used bioinformatic scripts

purpose
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

Python Libraries:

* screed

Installation
============

pip install bio_utils

Scripts
========

bio_utils contains several sub-packages containing scripts of similar function.
All scripts are written such that their functionality is importable
(aka the packages serve as Python libraries) but many scripts can also be run
independently. Any such script is linked to /usr/local/bin/.
Each sub-package and it's scripts are described below:

blast_tools
-----------

blast_tools contains a variety of scripts to assist with filtering and using
BLAST data. All scripts except blast_to_cigar are also stand-alone programs
and executable as "[script name]".

Scripts:
* blast_to_cigar: convert BLAST+ XML alignment lines to a CIGAR line
* filter_m8_evalue: filters a M8 (BLAST+ output format 6) file by e-value
* retrieve_query_sequences: recover query FASTA sequences for BLAST hits below
                            a given e-value
* retrieve_subject_sequences: recover subject FASTA sequences for BLAST hits
                              below a given e-value

iterators
---------

iterators simply contains a number of file iterators for reading, parsing, and
returning lines of a file as dictionaries. screed is used for reading
FASTQ files. See individual scripts for dictionary structure.

Scripts:
* fasta: reads, parses, and returns lines of a FASTA file
         {'name':, 'description':, 'sequence':}
         Note: This function is identical to the SCREED FASTA
               iterator but is theoretically faster.
* fastr: reads, parses, and returns lines of a FASTR file
         {'name':, 'description':, 'sequence':}
* gff3: reads, parses, and returns lines of a GFF3 file
        {'seqid':, 'source':, 'type':, 'start':, 'end':, 'score':,
        'strand':, 'phase':, 'attributes':} (Note: if 'prokka=True' is given,
        dynamic parsing of attributes as per the GFF3 file of PROKAA 1.12-beta
        is performed)
* m8: reads, parses, and returns lines of a M8 file (BLAST+ output format 6)
      {'queryID':, 'subjectID':, 'percIdentical':, 'alignLen':,
      'mismatchCount':, 'gapCount':, 'queryStart':, 'queryEnd':,
      'subjectStart':, 'subjectEnd':, 'eValue':, 'bitScore':}
* sam: reads, parses, and returns lines of a SAM file
       {'qname':, 'flag':, 'rname':, 'pos':, 'mapq':, 'cigar':, 'rnext':,
       'pnext':, 'tlen':, 'seq':, 'qual':}

verifiers
---------

verifiers contains scripts that examine a file type to ensure that the file is
formatted correctly. Each script returns True if the file is formatted
correctly and False if the file is incorrectly formatted. If the file is
incorrectly formatted, a description of the formatting error is printed. All
scripts in verifiers are also stand-alone programs and executable
 as "[script name]_verifier".

Scripts:
* binary: guesses whether or not a file is binary
* fasta: verifies a FASTA file
* fastq: verifies a FASTQ file
* fastr: verifies a FASTR file
* gff3: verifies a GFF3 file
* m8: verifies a M8 file (BLAST+ output format 6)
* sam: verifies a SAM file

mothur_tools
------------

mothur_tools contains scripts that perform various modifications to MOTHUR
(Patrick Schloss) files in order to modify output or functionality. All
scripts in mothur_tools are stand-alone programs and executable as
"[script_name]"

Scripts:
* convert_count_to_shared: effectively bypasses OTU generation while allowing normal
                           downstream MOTHUR analysis by converting a MOTHUR count_table
                           file to a MOTHUR shared file
* group_from_filenames: creates a MOTHUR group file from one or more FASTA files,
                        this script is much easier to use then allowing MOTHUR to
                        create the group file
* modify_tax_summary: modify the taxonomy summary file from MOTHUR
                      by adding full phylogeny to the taxon field
                      and optionally create taxonomy summary files
                      truncated to a specific taxon rank

Contributors
============

Alex Hyer (theonehyer@gmail.com)

Chris Thornton (christopher.thornton@utah.edu)

William Brazelton