====================================================
bio_utils: library of common bioinformatic functions
====================================================

:Authors: Alex Hyer, William Brazelton, Christopher Thornton
:Date: |today|
:Version: |version|

.. image:: images/bio_utils_logo_120.png

.. automodule:: bio_utils


Summary
=======

bio_utils is a library of Python modules performing routine functions in
bioinformatic scripts.


Introduction
============

Many bioinformatic scripts perform similar or identical tasks internally
during the execution of a program. Such tasks include reading FASTA files or
filtering BLAST+ results. bio_utils contains numerous functions that quickly
and simply handle simple, mundane, everyday tasks in a streamlined and simple
fashion to save developers time. bio_utils aims to be as simple as possible,
providing functionality without adding in unnecessary features, i.e. bio_utils
is as vanilla as reasonable. This both increases the speed of most functions
and greatly simplifies APIs.

Many libraries, such as
`SCREED <https://screed.readthedocs.io/en/v0.9/>`_ and
`Biopython <http://biopython.org/>`_, already provide importable functions that
execute these simple tasks. SCREED maintains a fairly simple API but is fairly
slow and no one has updated the original repo since 2012-06-17. Numerous
developers actively maintain Biopython and it is quite a bit faster, in some
regards, than SCREED. However, Biopython stocks their functions with an
enormous number of features that, while useful in a Python interpreter, are
often ignored by programs or can be accomplished more quickly using built-in
Python features, i.e. Biopython is bloatware to many developers. As
aforementioned, bio_utils' vanilla design overcomes both these libraries issues
by providing both simplicity and speed.

At this point in time, bio_utils is quite small and its scope limited. The
authors intend to slowly but surely increase this library's repertoire over
time. We welcome any and all contributions to our project.


Installation
============

::

    pip install bio_utils


Contents
========

.. toctree::
   :maxdepth: 2

   classes.rst
   iterators.rst
   verifiers.rst
   blast_tools.rst
   contributing.rst
   roadmap.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Copyright
=========

bio_utils' operates under the :download:`GPLv3 License <LICENSE.txt>` and may
be edited and redistributed as per that license.
