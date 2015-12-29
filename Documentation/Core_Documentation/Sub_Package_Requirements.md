Sub_Package_Requirements
========================

*Author: Alex Hyer*

The following principles from [Philosophy](Philosophy.md) directly apply to
sub-packages:

1. Intuitive
2. As Simple As Possible
3. Heavily Documented
4. Logically Organized
5. Up-to-Date

This document serves as a practical coding guide to implement these concepts
into sub-packages. The following list summarizes the requirements of
sub-packages in bio_utils, each item is then discussed in detail:

1. Try for 2+ scripts per package
2. Avoid "Miscellaneous" packages
3. Import at the package level
4. Document in [Documentation](Documentation)

Try for 2+ scripts per package
--------------------------------

While you can have a package with just a single script, try for at least two
scripts per package. There reasoning behind this is simple, a package with a
single script feels like an unnecessary ".package." in the import statement
and chances are you can think of a second script useful to the concept of a
package. If the latter is true, write that script.

Avoid "Miscellaneous" packages
------------------------------

Every script has an overarching category it can fit into, do so by putting it
in a package of said category (or make one). It is better to have a package
with one script than to have a Miscellaneous package.

Import at the package level
---------------------------

Since each script should have only one (or a few functions), they should be
imported at the package level (in the "__init__.py" file) so that a programmer
doesn't have to write redundant words in import statements. For example:

from bio_utils.iterators import sam_iter (package level = better)

from bio_utils.iterators.sam import sam_iter (file level = worse)

Document in [Documentation](Documentation)
------------------------------------------

Whereas functions should be heavily documented in their scripts, packages
should be primarily documented in
[Sub_Package_Documentation](Sub_Package_Documentation). This should include a
synopsis of what the package contains and a short description of each function,
what arguments it has, what it returns, and a simple usage example. Each
sub-package must also have a brief synopsis in it's "__init__.py" file.
