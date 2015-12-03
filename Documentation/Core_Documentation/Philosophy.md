Philosophy
==========

*Author: Alex Hyer*

Due to the *potential* size and number of contributors to this project, it is
helpful to have an underlying, general philosophy concerning what should be
included in bio_utils, how it should be coded, and where it should go within
the library. This ensures that everything is structured logically and that
the library is both intuitive to use and internally consistent. This document
explains these philosophies and should be read by anyone looking to contribute
to the library on whether or not their script belongs in bio_utils, where it
belongs, and how to structure their script A more concrete guide on how to
style a script in bio_utils is found in
[Script_requirements](Script_requirements.md).
[Sub_Package_Requirements](Sub_Package_Requirements.md) describes how and when
to make sub-packages in bio_utils.

Core Principles
---------------

1. Simple-to-Use/Intuitive: A software library is analogous to a toolkit. Like
a real-world toolkit, it should be organized so that any single tool can be
found without any real effort. Once a tool is found, it's function should be
obvious based on it's name, e.g. a screwdriver drives a screw through
material. To translate this analogy to computer terms, each script should be a
single tool whose name reflects its function.

2. ASAP (As Simple As Possible): A screwdriver drives a screw, a hammer applies
normal force, and a wrench applies torque. Each of these tools' use is fairly
singular and unique. Each script in a library should have a single,
unique function. To say that in more confusing terms: each tool should do one
thing and one thing only, and said thing shall not have already been done.
Additionally, each script should be written in a straightforward manner that
is easy to read and understand; i.e., each script should be
[Pythonic](http://blog.startifact.com/posts/older/what-is-pythonic.html).

3. Heavily Documented: A library is used by developers writing a program.
This obvious statement should lead to an obvious conclusion: a library is of no
use if a programmer doesn't know/can't find out what any given tool does. Thus,
each script should be very documented heavily. While, it is better to document
more than less, there is such a thing as too much documentation. There comes a
point where documentation is too repetitive and confuses the reader more than
helping them; avoid this.

4. Logically Organized: This point was basically made with the first Core
Principle but will be re-iterated/elaborated on here. When opening a toolkit,
it should be easy to figure out where a tool is because "tools of a feather
should be stored together". Therefore, a library should have a hierarchical
structure grouping similar tools. All tools fit into at least some catgeory
so there should never be a "miscellaneous" category.

5. Up-to-Date: An outdated library is not particularly useful. What constitutes
an outdated library can be quite variable as some tools may never need updating
after they're initially written. However, this is not normally the case as
new functionalities become desirable and various standards change. An
up-to-date library should always support the lastest file conventions and
adhere to current coding standards withing both
the library and the library's coding language.

6. Fast: The whole point of having a library is to save time and effort by
pre-writing tools and making them easily accessible. If the tools are slow
for their given task, they are essentially useless. Scripts should be written
so as to minimize resource usage and maximize speed. Occasionally, a script
that runs fast is not ASAP and vice versa. If such a conflict arises, attempt
to find an optimum intermediate favoring ASAP over speed.
