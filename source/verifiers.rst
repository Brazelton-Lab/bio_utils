=========
Verifiers
=========

.. automodule:: bio_utils.verifiers


Introduction
------------

The bio_util's verifiers subpackage contains numerous functions that verify the
data of a biological file format, i.e. they ensure a given file is properly
formatted. These function check file entries against a regex matching a
given file format. If the match fails, the verifier will subdivide the entry
and determine what part of the entry fails the regex. This investigation of the
entry permits the verifiers to return detailed error messages on what and where
the file failed.


entry_verifier
--------------

The guts of the verifiers package, this versatile function matches a string
to a regex. If the match fails, :func:`entry_verifier` splits both the regex
and string by a given delimiter and matches each regex fragment to its
corresponding string fragment. When a string fragment fails, a custom
:class:`FormatError` containing details on the failure is raised.

.. autofunction:: bio_utils.verifiers.entry_verifier


b6_verifier
-----------

Verifies the validity of a list of :ref:`B6Entry`.

.. autofunction:: bio_utils.verifiers.b6_verifier


binary_guesser
--------------

Heuristically guess whether a file is binary or text. While not technically a
"verifier", this function fits in this subpackage well as it helps confirm
a generic property of the file before use by a program.

.. autofunction:: bio_utils.verifiers.binary_guesser


fasta_verifier
--------------

Verifies the validity of a list of :ref:`FastaEntry`.

.. autofunction:: bio_utils.verifiers.fasta_verifier


fastq_verifier
--------------

Verifies the validity of a list of :ref:`FastqEntry`.

.. autofunction:: bio_utils.verifiers.fastq_verifier


gff3_verifier
-------------

Verifies the validity of a list of :ref:`GFF3Entry`.

.. autofunction:: bio_utils.verifiers.gff3_verifier


sam_verifier
------------

Verifies the validity of a list of :ref:`SamEntry`.

.. autofunction:: bio_utils.verifiers.sam_verifier
