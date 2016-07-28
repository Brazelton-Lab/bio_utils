=======
Classes
=======


Introduction
------------

bio_utils' offers many classes that house biological data from many different
file formats. Each instance contains an attribute per field of a given file
format as well as a ``write()`` method that returns the original entry properly
formatted and followed by a newline character. Each section below includes a
simple description of what each format contains and a link to a detailed
description of said format.

These classes are currently contained in the iterators subpackage but will
constitute their own package later, see `Roadmap <roadmap.rst>`_ for details.


.. _B6Entry:

B6Entry
-------

B6 files contain various data detailing the length and quality of an alignment
between nucleotide or protein sequences. This file format is used by
`NCBI BLAST+ <https://www.ncbi.nlm.nih.gov/books/NBK279690/>`_ as output format
6, hence B6 (Blast+ 6). B6 was referred to as M8 in NCBI BLAST.
`drive5 <http://www.drive5.com/usearch/manual/blast6out.html>`_ contains a
good, succinct description of this format. This class only supports the default
B6 format and does not accept arbitrary fields.

.. autoclass:: bio_utils.iterators.B6Entry
   :members:


.. _FastaEntry:

FastaEntry
----------

FASTA files contain nucleotide and protein sequences differentiated by unique
identifiers. `Wikipedia <https://en.wikipedia.org/wiki/FASTA_format>`_ provides
both the history of the FASTA format and format specifications.

.. autoclass:: bio_utils.iterators.FastaEntry
   :members:


.. _FastqEntry:

FastqEntry
----------

FASTQ files contain nucleotide and protein sequences differentiated by unique
identifiers, like :ref:`FASTA <FastaEntry>` files. FASTQ files also contain
quality scores indicating the confidence of each base or residue declaration.
`Wikipedia <https://en.wikipedia.org/wiki/FASTQ_format>`_ provides a
description of the FASTQ format and the meaning of the various quality scores.

.. autoclass:: bio_utils.iterators.FastqEntry
   :members:


.. _GFF3Entry:

GFF3Entry
---------

General Feature Format 3 (GFF3) contain various data on the location, type, and
quality of a nucleotide or protein sequence annotation. As opposed to previous
versions, GFF3 support an arbitrary number of hierarchical annotation levels.
`GMOD <http://gmod.org/wiki/GFF3>`_ gives a very detailed walkthrough of this
format.

.. autoclass:: bio_utils.iterators.GFF3Entry
   :members:


.. _SamEntry:

SamEntry
--------

Sequence Alignment/Map (SAM) files contains details on the location and quality
of an alignment. Many alignment programs produced SAM files as their default
output. `GitHub <https://samtools.github.io/hts-specs/SAMv1.pdf>`_ host a
painfully detailed description of the SAM file format.

.. autoclass:: bio_utils.iterators.SamEntry
   :members:
