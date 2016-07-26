=========
Iterators
=========


Introduction
============

The bio_utils' iterator subpackage contains numerous iterators for a variety
of biology-relevant file types. The contained iterators share numerous features
listed in the next section. The subsequent sections detail iterator-specific
elements. Each iterator returns file-specific Python classes. This page only
details how to use the iterators not the classes they return, see `classes.rst`
for details on each class in bio_utils.


Common Features
---------------

Abilities shared by all iterators in this package include:

* Return file-specific Python classes, see `classes.rst` for more details

* Support the ``next()`` and ``__next__()`` methods

* Usable in *for* loops

* Accept any iterator: ``iter()`` objects, file handles, memory files, etc.

* Begin iteration at arbitrary lines using *start_line* or *header* argument

All iterators in this package are quite fast;the following table compares
SCREED's, Biopython's, and bio_utils' FASTA iteration speed in seconds on a
3.2 GB FASTA file containing 1,614,108 sequence entries averaging 158 bases
each.

==========  =======  =======  =======  =======  =======  =======
 FASTA File Iteration Speed for Different Libraries (seconds)
----------------------------------------------------------------
Library     Trial#1  Trial#2  Trial#3  Trial#4  Trial#5  Average
==========  =======  =======  =======  =======  =======  =======
SCREED      974.812  971.185  953.027  961.247  971.924  966.439
Biopython   581.148  575.677  585.322  548.876  516.235  561.452
bio_utils   290.876  298.047  291.625  291.966  289.635  292.430
==========  =======  =======  =======  =======  =======  =======


B6/M8
-----

Iterates over B6 alignment files produced by numerous programs. B6 files
contain various data detailing the length and quality of an alignment between
nucleotide or protein sequences. This file format is used by
`NCBI BLAST+ <https://www.ncbi.nlm.nih.gov/books/NBK279690/>`_ as output format
6, hence B6 (Blast+ 6). B6 was referred to as M8 in NCBI BLAST.
`drive5 <http://www.drive5.com/usearch/manual/blast6out.html>`_ contains a
good, succinct description of this format. This iterator does not currently
support arbitrary table modifications as does BLAST+ but will support it in a
future release.  # TODO: Added class link!

.. autofunction:: bio_utils.iterators.b6_iter


FASTA
-----

FASTA files contain nucleotide and protein sequences differentiated by unique
identifiers. `Wikipedia <https://en.wikipedia.org/wiki/FASTA_format>`_ provides
both the history of the FASTA format and format specifications. This iterator
can handle FASTA sequences spanning multiple lines.  # TODO: Added class link!

.. autofunction:: bio_utils.iterators.fasta_iter


FASTQ
-----

FASTQ files contain nucleotide and protein sequences differentiated by unique
identifiers, like `FASTA`_ files. FASTQ files also contain quality scores
indicating the confidence of each base or residue declaration.
`Wikipedia <https://en.wikipedia.org/wiki/FASTQ_format>`_ provides a
description of the FASTQ format at the meaning of the various quality scores.
# TODO: Added class link!

.. autofunction:: bio_utils.iterators.fastq_iter


GFF3
----

General Feature Format 3 (GFF3) contain various data on the location, type, and
quality of a nucleotide or protein sequence annotation. As opposed to previous
versions, GFF3 support an arbitrary number of hierarchical annotation levels.
`GMOD <http://gmod.org/wiki/GFF3>`_ gives a very detailed walkthrough of this
format.  # TODO: Added class link!

.. autofunction:: bio_utils.iterators.gff3_iter


SAM
---

Sequence Alignment/Map (SAM) files contains details on the location and quality
of an alignment. Many alignment programs produced SAM files as their default
output. `GitHub <https://samtools.github.io/hts-specs/SAMv1.pdf>`_ host a
painfully detailed description of the SAM file format. Our iterator has not
been compared to `PySAM <https://pysam.readthedocs.io/en/latest/>`_ which is
likely faster and certainly has more features. There are no plans to support
BAM (Binary Alignment/Map) files as PySAM already provides a fast C-implemented
iterator for them.  # TODO: Added class link!

.. autofunction:: bio_utils.iterators.sam_iter
