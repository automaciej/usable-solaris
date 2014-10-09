Usable Solaris
==============

A collection of tools and application related to Solaris.

Preliminary Solaris 10 setup
----------------------------

If you've just installed Solaris 10 and you would like it to be a bit more
like Linux, see how to do a preliminary Solaris 10 setup.

SPARC box turnup HOWTO
----------------------

If you have a SPARC box without a CD-ROM and you're wondering how to install
Solaris on it, try this Solaris box turnup HOWTO.

Solaris package and patch database and browser
----------------------------------------------

If you have a number of Solaris hosts and you would like to know what packages
and patches are installed on which host, you can use this tool. The tool uses
ssh to remotely execute 'pkginfo' and 'showrev -p', then parses the output and
sticks it into a relational database (MySQL or PostgreSQL, or whatever else
Django supports). You can then run a web application and browse your
collection of machines.

The application can also do some reporting and simple analysis. It can find
packages that are installed in different versions on different machines, which
is useful to find outdated packages.
