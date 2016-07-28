============
Contributing
============


Introduction
============

Due to the *potential* size of this project and contributors thereto, it is
helpful to have an underlying, general philosophy concerning what should be
included in bio_utils, how it should be coded, and where it should go within
the library. This ensures that everything is structured logically and that
the library is both intuitive to use and internally consistent. This document
explains these philosophies—and their implementations—and should be read by
anyone looking to contribute to the library on whether or not their script
belongs in bio_utils, where it belongs, and how to structure their script.


How to Contribute
=================

This section is placed near the top for your convenience, if this is your first
time contributing, please read the rest of this document first.


Core Principles
===============


Simple-to-Use/Intuitive
-----------------------

A software library is analogous to a toolkit. Like a real-world toolkit, it
should be organized so that any single tool can be found without any real
effort. Once a tool is found, it's function should be obvious based on it's
name, e.g. a screwdriver drives a screw through material. To translate this
analogy to computer terms, each script should be a single tool whose name
reflects its function.


ASAP (As Simple As Possible)
----------------------------

A screwdriver drives a screw, a hammer applies normal force, and a wrench
applies torque. Each of these tools' use is fairly singular and unique. Each
script in a library should have a single, unique function. To say that in more
confusing terms: each tool should do one thing and one thing only, and said
thing shall not have already been done. Additionally, each script should be
written in a straightforward manner that is easy to read and understand; i.e.
each script should be
`Pythonic <http://blog.startifact.com/posts/older/what-is-pythonic.html>`_.


Heavily Documented
------------------

A library is used by developers writing a program. This obvious statement
should lead to an obvious conclusion: a library is of no use if a programmer
doesn't know/can't find out what any given tool does. Thus, each script should
be very documented heavily. While, it is better to document more than less,
there is such a thing as too much documentation. There comes a point where
documentation is too repetitive and confuses the reader more than helping them;
avoid this.


Logically Organized
-------------------

This point was basically made with the first Core Principle but will be
re-iterated/elaborated on here. When opening a toolkit, it should be easy to
figure out where a tool is because "tools of a feather should be stored
together". Therefore, a library should have a hierarchical structure grouping
similar tools. All tools fit into at least some category so there should never
be a "miscellaneous" category.


Up-to-Date
----------

An outdated library is not particularly useful. What constitutes an outdated
library is quite subjective as some tools may never need updating after they're
initially written. However, this is not normally the case as new functions
become desirable and various standards change. An up-to-date library should
always support the latest file conventions and adhere to current coding
standards withing both the library and the library's coding language.


Fast
----

The whole point of having a library is to save time and effort by pre-writing
tools and making them easily accessible. If the tools are slow for their given
task, they are essentially useless. Scripts should be written so as to minimize
resource usage and maximize speed. Occasionally, a script that runs fast is not
ASAP and vice versa. If such a conflict arises, attempt to find an optimum
intermediate favoring ASAP over speed.


Script Requirements
===================

This section is as a practical coding guide to implement the above principles
in bio_utils' scripts.


Follow PEP!
-----------

Python already has multiple cannon code style guides, versioning systems, etc.;
follow them! There are many PEPs so it can be hard to keep track of them all.
IDEs such as `PyCharm <https://www.jetbrains.com/pycharm/>`_ will take care of
PEP formatting for you. Several critical PEPs are also linked below:

* `PEP 0007 <https://www.python.org/dev/peps/pep-0007/>`_ - C Code Style Guide
* `PEP 0008 <https://www.python.org/dev/peps/pep-0008/>`_ - Python Code Style
Guide
* `PEP 0440 <https://www.python.org/dev/peps/pep-0440/>`_ - Versioning and
Specifying Dependencies


Only One or a Few Related Importable Functions per Script
---------------------------------------------------------

Each script should only contain a few related functions at most. Most scripts
should only have a single function. This helps keep everything logically and
hierarchically organized. Let's go over a simple example to demonstrate the
benefits of this approach:

One could write a script called fasta.py that contains all library functions
dealing with FASTA files. This seems convenient because if a developer wants
to do something with a FASTA file, s/he only needs to look at one script to see
if the functionality they want exists. However, they have to open and look
through the whole file to see if what they want exists. Also, they can't get
any information on categorical functions such as what iterators available in
bio_utils. By creating a sub-package called "iterators" in bio_utils and
placing a fasta.py script containing a single function (iterating through
a FASTA file), a developer can see what iterators are available and understand
the function of fasta.py at the same time without needing to open a file! Also,
by placing a fasta.py in each appropriate sub-package (with the package-
corresponding functionality), a developer can simply search for files named
fasta.py to glean everything they can do with a FASTA file in bio_utils.
This also makes imports more obvious and clear to a reader.

If multiple functions are all related to a single "thing" within the same
sub-package, then it is appropriate to include multiple functions in a single
script. Doing so is simply a best judgement call.


No "End" Functions
------------------

As aforementioned, a software library is analogous to a toolbox. To that end,
each script should perform and return data but never execute an ultimatum. The
developer needs to have maximal control over their script; they should not have
to worry about tools manipulating the flow of their program. As an example, all
functions in the verifiers sub-package used to exit the program if a file could
not be validated because it assumed that if a file was incorrectly formatted,
the program calling it would crash downstream. This assumption is not always
valid and such a drastic change in program flow should never be assumed. Now
all the verifiers raise a :class:`FormatError` if a file is invalid. This
allows programmers let a script crash with the error or catch and continue.

Since each script or function must act as a means and not an end, they **MUST**
return something. There is no such thing as a silent function call in
bio_utils.

In summary, scripts in bio_utils should never print to screen, exit the
program, or elsewise do anything a developer cannot control and must return
something. Scripts can raise errors.


No Command-Line Programs
------------------------

This section is somewhat related to the last, i.e. bio_utils is a library and
not an end product. As such, there are no standalone programs as that would
constitute an end goal. There is, however, one exception: if the function in
the script can be logically and simply transformed into a standalone program,
then it should be made into one. As an example, each of the verifiers double as
command-line programs that take a single file as their only argument and print
whether or not the file is properly formatted. When a script in bio_utils
doubles as a program, it should:

1. Simply call it's own importable function
2. The program should support the following (if applicable):
    * Reading and writing compressed files
    * Piping
    * One or zero positional arguments


Docstrings for Each Script, Class, AND Function
-----------------------------------------------

Each individual document in bio_utils should be documented with docstrings and
inline comments as appropriate. More specifically, each docstring should have
a synopsis line, document arguments, and returns as per
`Google Function Definitions <https://google.github.io/styleguide/pyguide.html?showone=Comments#Comments>`_
. If appropriate, the docstrings should also include a more thorough
description of the function. Each script, *even those only containing a single
function or class*, should also have docstrings. If the script contains one
function or class, the docstring can simply be a one-liner about the function
and copyright information. If the script has multiple functions or classes, the
docstrings should include a synopsis of what the script offers and a one-liner
about each function. Full API should also be described in our Sphinx


Metadata and Copyright
----------------------

All scripts must start with the following code:

.. code-block:: python

    #! /usr/bin/env python

    # from __future__ imports go here

    """<one-liner describing software>

    <whatever you want here>

    Copyright:

        <program name> <one-liner describing software>
        Copyright (C) 2015  William Brazelton, Alex Hyer

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
    """

    __author__ = '<authors>'
    __email__ = '<email of lead author or maintainer>'
    __license__ = 'GPLv3'
    __maintainer__ = '<maintainer of script>'
    __status__ = '<production level of script>'
    __version__ = '<script version>'
    __credits__ = '<credit for legally borrowed code if appropriate>'

    # imports, then rest of script


Sub-Package Requirements
========================

This section details what sub-packages in bio_utils contain and when it is
appropriate to start a new one.


2+ Scripts per Package
----------------------

While you can have a package with just a single script, try for at least two
scripts per package. The reasoning behind this is simple, a package with a
single script feels like an unnecessary "package" in the import statement
and chances are you can think of a second script useful to the concept driving
the sub-package. If a script truly doesn't fit in any other sub-package, try
to think of a second function fitting the schema and code it. bio_utils will
never have a "misc" package.


Import at Package Level
-----------------------

Since each script should have only one (or a few functions), they should be
imported at the package level—in the "__init__.py" file—so that a programmer
doesn't have to write redundant words in import statements. For example:

from bio_utils.iterators import sam_iter (package level = better)

from bio_utils.iterators.sam import sam_iter (file level = worse)


Own Documentation Page
----------------------

Each sub-package must have its own web page in the documentation following this
format::

    =====
    Title
    =====

    .. automodule:: <module>

    Introduction
    ------------

    <what package contains and any globally relevant information>

    <optional sections>

    <first function>
    ----------------

    <short function description, should be longer/give more info than function
    one-liner>

    .. autofunction:: <function>


