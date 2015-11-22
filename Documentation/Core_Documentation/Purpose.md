Purpose
=======

*Author: Alex Hyer*

Many modern biology labs already employ [bioinformatics]
(https://en.wikipedia.org/wiki/Bioinformatics) to analyze [NGS]
(https://www.ebi.ac.uk/training/online/course/ebi-next-generation-sequencing-practical-course/what-you-will-learn/what-next-generation-dna-)
(Next Generation Sequencing) data and the number of said labs increases
annually. As a result, an increasingly large quantity of code is being written
in these labs; a significant proportion of this code is functionally repetitive
yet non-standardized and thus non-portable. Standardization of code is
advantageous for the following reasons:

1. Standardization prevents the unnecessary repetition of code.
2. Standardized code is often simple and portable and thus improves code
versatility, e.g. a FASTA file reader written quickly by a scientist for a
single script may only return certain relevant information, but a standardized
FASTA file reader will be utilizable by any script needing to read a FASTA
file.
3. Standardized code has already been written, thus saving
time for the programmer. The amount of time saved by not re-writing simple
code on a regular basis is substantial.

There are two projects that are already attempting to standardize bioinformatic
code in Python to the knowledge of this package's authors: 
[SCREED](https://github.com/ctb/screed) and
[Biopython](http://biopython.org/wiki/Main_Page). Both of these projects have
shortcomings that justify the creation of a new Python bioinformatic developer
library. The primary SCREED repository has not been updated in over four years
and is quite small (though it is quite powerful for it's small size).
Biopython, on the other hand, is monolithic and feature-rich to a fault. The
sheer size and complexity of Biopython can create a sharp sigmoidal learning
curve and the hierarchical package organization is not always intuitive.
Biopython is very feature rich but many of the features are excessive, rarely
used, only practical in a Python interpreter session, and/or not suited for
large data sets. These feature traits cause Biopython to be quite slow and
memory/CPU intensive.

bio_utils aims to be a KISS (Keep It Simple Stupid) based bioinformatic
development library that is:

1. Simple to Use
2. ASAP (As Simple As Possible)
3. Heavily Documented (but not excessively documented, no one wants to read
huge manuals)
4. Logically Organized
5. Up-to-Date
6. Fast

In short, bio_utils aims to be a smaller, more focused, and significantly
faster version of Biopython.
