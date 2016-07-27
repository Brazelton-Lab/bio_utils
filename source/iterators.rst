=========
Iterators
=========


Introduction
------------

The bio_utils' iterator subpackage contains numerous iterators for a variety
of biology-relevant file types. The contained iterators share numerous features
listed in the next section. The subsequent sections detail iterator-specific
elements. Each iterator returns file-specific Python classes. This page only
details how to use the iterators not the instances they return, see
`Classes <classes.rst>`_ for details on each class in bio_utils.


Common Features
---------------

Abilities shared by all iterators in this package include:

* Return file-specific instances, see `Classes <classes.rst>`_ for more details

* Support the ``next()`` and ``__next__()`` methods

* Usable in *for* loops

* Accept any iterator: ``iter()`` objects, file handles, memory files, etc.

* Begin iteration at arbitrary lines using *start_line* or *header* argument

All iterators in this package are quite fast; the following table compares
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


b6_iter
-------

Iterates over B6 alignment files and returns each line as an instance of
:ref:`B6Entry`. This iterator does not support arbitrary table modifications as
does BLAST+.

.. autofunction:: bio_utils.iterators.b6_iter


fasta_iter
----------

Iterates over a FASTA file and returns each entry as an instance of
:ref:`FastaEntry`. This iterator can handle sequences spanning multiple lines.

.. autofunction:: bio_utils.iterators.fasta_iter


fastq_iter
----------

Iterates over a FASTQ file and returns each entry as an instance of
:ref:`FastqEntry`. This iterator can handle sequences and quality score
spanning multiple lines.

.. autofunction:: bio_utils.iterators.fastq_iter


gff3_iter
---------

Iterates over a GFF3 file and returns each line as an instance of
:ref:`GFF3Entry`.

.. autofunction:: bio_utils.iterators.gff3_iter


sam_iter
--------

Iterates over a SAM file and returns each as line as an instance of
:ref:`SamEntry`.

.. autofunction:: bio_utils.iterators.sam_iter
