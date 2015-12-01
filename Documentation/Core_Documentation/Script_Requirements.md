Script Requirements
===================

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
2. One or a Few (Related) Importable Functions per Script
3. No "End" Scripts or Functions
4. No Command Line Programs (see section for exception)
* Support Compression and Decompression
* Support Piping
* Minimal to No Positional Arguments
5. All Functions Return Something
6. Docstrings for Each Script AND Function
7. Sphinx Function Definitions for Function Docstrings
8. Write Unit Tests
