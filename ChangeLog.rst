Changelog
=========

%%version%% (unreleased)
------------------------

- Fixed errors if gff3_iter, added test_gff3_iter. [TheOneHyer]

  gff3_iter was returning an empty dictionary value when
  a semicolon is at the end of the attributes line and attributes
  were not ordered and thus returned in the same format they were
  read. Both issues fixed. Added test_gff3_iter.
  Comments added to certain scripts to prevent PyCharm from
  throwing false-positive warning about iterators.

- Added test_gff3_iter and updated GFF3_iter. [TheOneHyer]

  Updated gff3_iter to have ints where appropriate.
  Added incomplete test_gff3_iter

- Fixed b6_iter and added unit test. [TheOneHyer]

  Added test_b6_iter. Changed b6_iter values to ints
  and floats as appropriate. write() still writes as string.

- Fixed Error in fastq_iter, added test_fastq_iter. [TheOneHyer]

  fastq_iter had a major error, was fixed. test_fastq_iter added.
  test_fasta_iter has new function to test header line ability.

- Updated Iterators and Added First Unit Test. [TheOneHyer]

  Created tests directory, fasta_iter unit test, and
  updated iterators to take any iterator.

- Updated gitignore and ChangeLog. [TheOneHyer]

  Last commit didn't include changes to gitignore or
  ChangeLog, rectifying

- Removed .pypirc. [TheOneHyer]

  .pypirc was being inappropriately tracked, has been removed.

- Giant Changes. [TheOneHyer]

  This commit sadly breaks normal rules of small commits
  and will be the lsat of it's kind. This commit implements
  huge changes and thus this commit message is giant.

  * Added GitChangeLog package and created first ChangeLog.rst

  * Updated Docuemntation

  * Updated READEME

  * Changed Copyright to GPLv3

  * Added proper copyright infor to each file

  * Greatly improved speed and flexibility of iterators

  * Added FASTQ iterator

  * Changed all isntances of 'm8' to 'b6' as appropriate

  * Iterators tested for functionality

  * verifiers updated for iterator changes, NOT TESTED

  * blast_tools updated for iterator changes, NOT TESTED

  * function documentation made 'Sphinxy'

  * Created directory for future Sphinx documentation

  * Added more package level imports

- Updated README.md. [TheOneHyer]

  README.md updated to match recent changes.

0.7.12 (2016-03-03)
-------------------

- Modified setup.py. [TheOneHyer]

  Last commit did not remove all necessary links from setup.py,
  this has been corrected.

- Deleted Mothur Scripts. [TheOneHyer]

  The mothur_tool scripts broke the argument that all scripts
  in a library should primarily be importable functions and not standalone
  programs. They have been removed.

0.7.11 (2015-12-29)
-------------------

- Finished Core Documentation. [Alex Jay Hyer]

  All planned core documents are complete.

- Updated Documentation. [Alex Jay Hyer]

  Minor documentation updates in COre_Documentation

- Core_Documentation Updates. [Alex Jay Hyer]

  Added content to all files in Core_Documentation and added
  the document Sub_Package_Requirements.

- Added Core Documentation. [Alex Jay Hyer]

  Added and updated core documentation including Philosophy.md,
  Documentation_Overview.md, and Script_Requirements.md

- Minor speeling fixes to Philosophy.md. [Alex Jay Hyer]

- Began Creating Project Documentation. [Alex Jay Hyer]

  bio_utils is now aiming at becoming a more powerful bioinformatic
  developer library. This commit provides documentation explaining
  projext goals and philosophies.

- Fixed file writing error. [Alex Jay Hyer]

0.7.10 (2015-11-04)
-------------------

- Fixed options error in retrieve_subject_sequences.py. [Alex Jay Hyer]

0.7.9 (2015-11-04)
------------------

- Fixed NameError bug in retrieve_subject_sequences.py. [Alex Jay Hyer]

0.7.8 (2015-10-22)
------------------

- Updated version numbers and improved imports. [Alex Jay Hyer]

  Version numbers now all adhere to PEP standards.
  Sub-package __init__.py files updated so that
  imports are simplier. See README.md for details
  on importing.

0.7.7 (2015-10-08)
------------------

- Fixing merge issues. [Alex Jay Hyer]

- Fixing merging issues. [Alex Jay Hyer]

- Merge branch 'master' of https://github.com/Brazelton-Lab/bio_utils.
  [Alex Jay Hyer]

  Conflicts:
  	bio_utils/mothur_tools/modify_tax_summary.py
  	setup.py

- Update setup.py. [Alex Hyer]

  Incremented version number

- Update modify_tax_summary.py. [Alex Hyer]

  Changed FileChecker to IOChecker

- Update setup.py. [Alex Hyer]

  Incremented version number

- Update modify_tax_summary.py. [Alex Hyer]

  Fixed bug in file checking

- Bug fix to modify_tax_summary.py. [Alex Jay Hyer]

- Added group_from_filenames under Mothur_tools. [Alex Jay Hyer]

  group_from_filenames creates MOTHUR formatted group
  files from FASTA fiel anmes. Thsi is much easier to do then
  allowign MOTHUR to create the group file itself.

- ANother minor bug fix. [Alex Jay Hyer]

- Minor bug fix. [Alex Jay Hyer]

- Added convert_count_to_shared.py. [Alex Jay Hyer]

  convert_count_to_shared added to mothur_tools. This script
  effectively bypasses OTU generation in MOTHUR whiel allowing
  downstream analysis.

- Fixed error output in modify_tax_summary and updated README. [Alex Jay
  Hyer]

- Finalized file_check and modify_tax_summary. [Alex Jay Hyer]

  Documentation in README.md will follow soon. file_check now contains
  the class IOChecker which performs all file checking actions.
  modify_tax_summary has a slightly different user interface and is
  fully functional.

- Made changes to modify_tax_summary input. [Alex Jay Hyer]

- Fixed bug in modify_tax_summary. [Alex Jay Hyer]

- Added modify_tax_summary to console scripts. [Alex Jay Hyer]

- Added file_tools and mothur_tools. [Alex Jay Hyer]

  All files now up to PEP standards. file_Tools created to house generic
  file related tools. It currently contains a permission checking system
  for reading and writing files. mothur_tools added to hold tools related
  to assisst in processing files for and from Mothur. Currently contains
  a taxonomy summary editing script.

- Blast_tools now also executable. [Alex Jay Hyer]

- Modified scripts so that console_scripts works. [Alex Jay Hyer]

- Testing creation of console scripts. [Alex Jay Hyer]

- Fixed FASTA iter. [Alex Jay Hyer]

- Fixed FASTA iter. [Alex Jay Hyer]

- Fixed FASTA iter. [Alex Jay Hyer]

- Fixed FASTA iter. [Alex Jay Hyer]

- Added FASTA iter. [Alex Jay Hyer]

- Fixed FASTA stop from alst commit. [Alex Jay Hyer]

- Fixed gff3_iter to stop reading before FASTA entries. [Alex Jay Hyer]

- Gff3_iter can now further parse attributes. [Alex Jay Hyer]

- Gff3_iter can now further parse attributes. [Alex Jay Hyer]

- Fixed import errors. [Alex Jay Hyer]

- Edited README. [TheOneHyer]

  README now looks better

- Fixed Bug. [TheOneHyer]

  Fixed bug from last update

- Update setup.py. [TheOneHyer]

  setup.py now properly shows where packages are

- Don't Worry. [TheOneHyer]

  Don't Worry

- Minor changes. [TheOneHyer]

  Some minor changes, mostly with PEP formatting but more still needs to
  be done

- Added retrieve_query_sequences.py. [TheOneHyer]

  added retrieve_query_sequences.py to retrieve the query sequences of
  BLAST hits from an M8 (BLAST+ output format 6) file. updated
  retrieve_subject_sequences.py to remove bug where repeats were erased.

- Added blast_tools and documentation. [TheOneHyer]

  added blast_tools which consists of scripts to assist with interpreting
  and using BLAST data. Added documentation to stand-alone scripts. All
  scripts tested and fully functional

- README Update. [TheOneHyer]

  README updated to actually be a README

- Verifiers work as stand-alone scripts. [TheOneHyer]

  All the file verifiers now work as stand alone programs in addition to
  their previous function  as an importable module. Each verifier simply
  takes a single argument which is the file to verify and prints whether
  or no the file is valid.

- Initial Commit. [TheOneHyer]

  A package of Python Modules containing generally useful bioinformatic
  scripts

- Initial commit. [Alex Hyer]


