# Copyright 2009 OpenCSW
# Distributed under the terms of the GNU General Public License v2
# $Header: $

GARNAME = log4sh
GARVERSION = 1.4.2
CATEGORIES = server

DESCRIPTION = A logging framework for shell scripts
define BLURB
  http://log4sh.sourceforge.net/

  log4sh is an advanced logging framework for shell scripts (eg. sh, bash) that
  works similar to the logging products available from the Apache Software
  Foundataion (eg. log4j, log4perl).
endef

MASTER_SITES = $(SF_MIRRORS)
DISTFILES  = $(GARNAME)-$(GARVERSION).tgz
DISTFILES += $(call admfiles,CSWlog4sh,)

# We define upstream file regex so we can be notifed of new upstream software
# release
UFILES_REGEX = $(GARNAME)-(\d+(?:\.\d+)*).tgz

CONFIGURE_SCRIPTS =
TEST_SCRIPTS =
BUILD_SCRIPTS =
INSTALL_SCRIPTS = custom

install-custom:
	ginstall -d $(DESTDIR)$(libdir)/log4sh
	ginstall $(WORKSRC)/src/shell/log4sh $(DESTDIR)$(libdir)/log4sh/log4sh
	ginstall -d $(DESTDIR)$(sharedir)/doc
	ginstall -d $(DESTDIR)$(sharedir)/doc/log4sh
	ginstall $(WORKSRC)/doc/FAQ.txt $(DESTDIR)$(sharedir)/doc/log4sh
	ginstall $(WORKSRC)/doc/log4sh.html $(DESTDIR)$(sharedir)/doc/log4sh
	ginstall $(WORKSRC)/doc/README.html $(DESTDIR)$(sharedir)/doc/log4sh
	ginstall $(WORKSRC)/doc/contributors.txt $(DESTDIR)$(sharedir)/doc/log4sh

include gar/category.mk
