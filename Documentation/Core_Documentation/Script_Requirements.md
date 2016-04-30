Script Requirements
===================

*Author: Alex Hyer*

As mentioned in [Philosophy](Philosophy.md), scripts should be:

1. Intuitive
2. As Simple As Possible
3. Heavily Documented
4. Logically Organized
5. Up-to-Date
6. Fast

This document serves as a practical coding guide to implement these concepts
into code as well as a list of what each script requires. The following is a
list summarizing script requirements, each item is then discussed in detail:

1. Follow PEP!
2. Only One or a Few Related Importable Functions per Script
3. No "End" Scripts or Functions
4. No Command-Line Programs (see section for exception)
5. Docstrings for Each Script, Class, AND Function
6. Versioning
7. Unit Tests

Follow PEP!
-----------

Python already has multiple cannonized code style guides, versioning system,
etc.; follow them! There are many PEPs so it can be hard to keep track of them
all. IDEs such as [PyCharm](https://www.jetbrains.com/pycharm/) will take care
of PEP formatting for you. Several critical PEPs are also linked below:

* [PEP 0007](https://www.python.org/dev/peps/pep-0007/) - C Code Style Guide
* [PEP 0008](https://www.python.org/dev/peps/pep-0008/) - Python Code Style
Guide
* [PEP 0440](https://www.python.org/dev/peps/pep-0440/) - Versioning and
Specifying Dependencies

Only One or a Few Related Importable Functions per Script
---------------------------------------------------------

Each script should only contain a few related function at most. Most scripts
should only have a single function. This helps keep everything logically and
hierarchically organized. Let's go over a simple example to demonstrate the
benefits of this approach:

One could write a script called fasta.py that contains all library functions
dealing with FASTA files. This seems convenient because if a developer wants
to do something with a FASTA file, s/he only needs to look at one script to see
if the functionality they want exists. However, they have to open and look
through the whole file to see if what they want exists. Also, they can't get
any information on categorical functions such as which iterators available in
bio_utils. By creating a sub-package called "iterators" in bio_utils and
placing a fasta.py script containing a single function [to iterate through
a FASTA file], a developer can see what iterators are available and understand
the function of fasta.py at the same time without needing to open a file! Also,
by placing a fasta.py in each appropriate sub-package (with the package-
corresponding functionality), a developer can simply search for files named
fasta.py to glean everything they can do with a FASTA file in bio_utils.
This also makes imports more obvious and clear to a reader.

If multiple functions are all related to a single "thing" within the same
sub-package, then it is appropriate to include multiple functions in a single
script. Doing so is simply a best judgement call.

No "End" Scripts or Functions
-----------------------------

As mentioned innumerous times in [Philosophy](Philosophy.md), a software
library is analogous to a toolbox. To that end, each script should perform
and return data but never perform an ultimatum. The developer needs to have
maximal control over their script; they should not have to worry about tools
manipulating the flow of their program. As an example, all functions in the
iterators sub-package used to exit the program if a file could not be
validated because it assumed that if a file was incorrectly formatted, the
program calling it would crash downstream. This assumption is not always valid
and such a drastic change in program flow should never be assumed. Now all the
verifiers return True or False if the file is correctly or incorrectly
formatted respectively.

Since each script or function must act as a means and not an end, they **MUST**
return something. There is no such thing as a silent function call in
bio_utils.

In summary, scripts in bio_utils should never print to screen, exit the
program, or elsewise do anything a developer cannot control and must return
something.

No Command-Line Programs
------------------------

This section is somewhat related to the last, i.e. nothing in bio_utils is an
end goal and bio_utils is a library. As such, there are no standalone programs
as that would constitute an end goal. However, there is one exception: if the
function in the script can be logically and simply transformed into a
standalone program, then it should be made into one. As an example, each of the
verifiers double as command-line programs that take a single file as their only
argument and print whether or not the file is properly formatted. When a script
in bio_utils doubles as a program:

1. The program functionality of the script should simply call it's own function
and still be able to act as an importable tool.
2. The program should support the following (if applicable):
    * Reading and writing compressed files
    * Piping
    * One or zero positional arguments

Docstrings for Each Script, Class, AND Function
------------------------------------------------

Each individual document in bio_utils should be documented with docstrings and
inline comments as appropriate. More specifically, each docstring should have
an synopsis line and document arguments and returns using
[Google Function Definitions](https://google.github.io/styleguide/pyguide.html?showone=Comments#Comments)
. If appropriate, the docstrings should also include a more thorough
description of the function. Each script, *even those only containing a single
function or class*, should also have docstrings. If the script contains one
function or class, the docstring can simply be a one-liner about the function.
If the script has multiple functions or classes, the docstrings should include
a synopsis of what the script offers and a one-liner about each function.
Full API should also be described in our Sphinx documentation.

Versioning
----------

Each sub-package and script must have a version number that is incremented
each time it is edited as well as a \__date__ variable containing the date the
script was last edited.

Unit Tests
----------

Since libraries are large and often intra-dependent, thorough unit tests are
required for all scripts to ensure that future changes do not break the library
. **Currently we use [pytest](http://pytest.org/latest/), this may change based
on needs; it will be cemented soon-ish.**