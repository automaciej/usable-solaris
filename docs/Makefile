# $Id$
#
# Required packages:
# - asciidoc
# - tofrodos

all: \
	opencsw-solaris-packages.html \
	solaris-10-preliminary-setup.html \
	sparc-box-turnup.html

%.html: %.txt
	asciidoc -a toc -a numbered $<
	fromdos $@
