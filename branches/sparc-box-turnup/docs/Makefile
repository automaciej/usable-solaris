# Required packages:
# - asciidoc
# - tofrodos

all: sparc-box-turnup.html solaris-10-preliminary-setup.html

%.html: %.txt
	asciidoc -a toc -a numbered $<
	fromdos $@
