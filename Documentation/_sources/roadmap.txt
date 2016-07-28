=======
Roadmap
=======


Introduction
------------

This page details planned updates and features for future versions of
bio_utils. There is not a timetable for any of these upgrades. The following
changes may themselves change frequently and drastically.


V1.1
----

* Give all iterators an argument to verify each entry before returning

* Added iterator for forward and reverse reads


V1.2
----

* Create a new package for file tools

* Add versatile compression reader based on `<http://stackoverflow.com/a/13044946/1585509>`_

* Add versatile compression writer


V2.0
----

This major version change will include many changes that make bio_utils API
more intuitive and better organized. While some changes seem smaller, like
renaming packages, they constitute a major as they will break current API and
not be backwards compatible.

* Rename iterators package to readers, many doc changes

* Moving classes in iterators to a new "data storage structures" package