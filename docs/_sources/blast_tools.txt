===========
Blast Tools
===========

.. automodule:: bio_utils.blast_tools


Introduction
------------

The bio_utils' blast_tools subpackage contains a few tools for making BLAST
output easier to work with. They are from extensive but what they do provide
may be useful to some developers.


blast_to_cigar
--------------

A simple function that converts the query sequence, subject sequence, and
midline fields of BLAST+ XML output (M7) to a
`CIGAR string <http://drive5.com/usearch/manual/cigar.html>`_. This function
supports both the newer and older versions of CIGAR strings.

.. autofunction:: bio_utils.blast_tools.blast_to_cigar


b6_evalue_filter
----------------

This function iterates through any iterator yielding lines of a
:ref:`B6/M8 <B6Entry>` file. This iterator only returns the lines above an
E-value threshold as :ref:`B6Entry`.

.. autofunction:: bio_utils.blast_tools.b6_evalue_filter


query_sequence_retriever
------------------------

Retrieve the aligned query sequence for each alignment in a B6 file above an
E-value threshold.

.. autofunction:: bio_utils.blast_tools.query_sequence_retriever


subject_sequence_retriever
--------------------------

Identical to `query_sequence_retriever`_ except it returns subject sequences.

.. autofunction:: bio_utils.blast_tools.subject_sequence_retriever

