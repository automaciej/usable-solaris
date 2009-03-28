GARNAME = minimalsmf
GARVERSION = 0.1
CATEGORIES = server

DESCRIPTION = This is a test of an smf-enabled package.
define BLURB
  The program just sleeps. It's about writing SMF manifests and stuff.
endef

ARCHALL = 1
MASTER_SITES = 
DISTFILES  = sleeping-beauty
DISTFILES += $(call admfiles,CSWminimalsmf,)
DISTFILES += csw$(GARNAME) csw$(GARNAME).xml svc-csw$(GARNAME)

REQUIRED_PKGS = CSWcswclassutils
SPKG_CLASSES = none cswinitsmf
PROTOTYPE_FILTER  = awk '$$$$3 ~ /\/init.d\/cswminimalsmf$$$$/ { $$$$2 = "cswinitsmf" } { print }'


CONFIGURE_SCRIPTS =
BUILD_SCRIPTS =
TEST_SCRIPTS =
INSTALL_SCRIPTS = minimalsmf

include gar/category.mk

install-minimalsmf:
	ginstall -d $(DESTDIR)
	ginstall -d $(DESTDIR)$(bindir)
	ginstall -m 755 files/sleeping-beauty $(DESTDIR)$(bindir)

