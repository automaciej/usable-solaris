# Copyright 2009 OpenCSW
# Distributed under the terms of the GNU General Public License v2
# $Header: $

GARNAME = portage
GARVERSION = 2.1.6.9
CATEGORIES = apps

PATCHVER = $(GARVERSION)
MAJ_VERSION = 2.1.6

DESCRIPTION = Gentoo portage
define BLURB
  It does stuff with things
endef

MASTER_SITES = http://ftp.heanet.ie/pub/gentoo/distfiles/
DISTFILES  = $(GARNAME)-$(MAJ_VERSION).tar.bz2

WORKSRC = $(WORKDIR)/$(GARNAME)-$(MAJ_VERSION)
ARCHALL = 1
CONFIGURE_SCRIPTS =
BUILD_SCRIPTS =
TEST_SCRIPTS =
INSTALL_SCRIPTS = portage
PATCHFILES  = $(GARNAME)-$(PATCHVER).patch.bz2
PATCHFILES += $(GARNAME)-$(PATCHVER)-solaris.patch

include gar/category.mk

portage_base = $(prefix)/portage
portage_share_config=$(prefix)/share/portage/config

bz-patch-$(GARNAME)-$(PATCHVER).patch.bz2:
	bzcat $(DOWNLOADDIR)/$(GARNAME)-$(PATCHVER).patch.bz2 | gpatch -d $(WORKSRC) -p0

install-portage:
	ginstall -d $(DESTDIR)/etc
	ginstall $(WORKSRC)/cnf/etc-update.conf $(DESTDIR)/etc
	ginstall $(WORKSRC)/cnf/dispatch-conf.conf $(DESTDIR)/etc
	ginstall -d $(DESTDIR)$(portage_share_config)
	ginstall $(WORKSRC)/cnf/make.conf $(DESTDIR)$(portage_share_config)/make.conf.example
	ginstall $(WORKSRC)/cnf/make.globals $(DESTDIR)$(portage_share_config)
	gln -s ..$(portage_share_config)/make.globals $(DESTDIR)/etc
	ginstall -d $(DESTDIR)$(sysconfdir)
	ginstall -d $(DESTDIR)$(sysconfdir)/logrotate.d
	ginstall $(WORKSRC)/cnf/logrotate.d/elog-save-summary $(DESTDIR)$(sysconfdir)/logrotate.d
	ginstall -d $(DESTDIR)$(portage_base)/bin
	for f in $(wildcard $(WORKSRC)/bin/*); do \
		ginstall -m 755 "$$f" $(DESTDIR)$(portage_base)/bin; \
	done
	ginstall -d $(DESTDIR)$(portage_base)/bin/ebuild-helpers
	gfind $(WORKSRC)/bin/ebuild-helpers -type f ! -type l \
		-exec ginstall {} $(DESTDIR)$(portage_base)/bin/ebuild-helpers \;
	gfind $(WORKSRC)/bin/ebuild-helpers -type l \
		-exec ginstall {} $(DESTDIR)$(portage_base)/bin/ebuild-helpers \;
	gln -s ../portageq $(DESTDIR)$(portage_base)/bin/ebuild-helpers/portageq
	for x in eerror einfo ewarn eqawarn; do \
		gln -s elog $(DESTDIR)$(portage_base)/bin/ebuild-helpers/$$x; \
	done
	# This could be probably made into a loop.
	ginstall -d $(DESTDIR)$(portage_base)/pym/portage
	ginstall $(wildcard $(WORKSRC)/pym/portage/*.py) \
		$(DESTDIR)$(portage_base)/pym/portage
	# TODO: some more symlinks
	ginstall -d $(DESTDIR)$(portage_base)/pym/_emerge
	ginstall $(wildcard $(WORKSRC)/pym/_emerge/*.py) \
		$(DESTDIR)$(portage_base)/pym/_emerge
	ginstall -d $(DESTDIR)$(portage_base)/pym/repoman
	ginstall $(wildcard $(WORKSRC)/pym/repoman/*.py) \
		$(DESTDIR)$(portage_base)/pym/repoman
	ginstall -d $(DESTDIR)$(portage_base)/pym/portage/env
	ginstall $(wildcard $(WORKSRC)/pym/portage/env/*.py) \
		$(DESTDIR)$(portage_base)/pym/portage/env
	ginstall -d $(DESTDIR)$(portage_base)/pym/portage/proxy
	ginstall $(wildcard $(WORKSRC)/pym/portage/proxy/*.py) \
		$(DESTDIR)$(portage_base)/pym/portage/proxy
	ginstall -d $(DESTDIR)$(portage_base)/pym/portage/_sets
	ginstall $(wildcard $(WORKSRC)/pym/portage/_sets/*.py) \
		$(DESTDIR)$(portage_base)/pym/portage/_sets
	ginstall -d $(DESTDIR)$(portage_base)/pym/portage/cache
	ginstall $(wildcard $(WORKSRC)/pym/portage/cache/*.py) \
		$(DESTDIR)$(portage_base)/pym/portage/cache
	ginstall -d $(DESTDIR)$(portage_base)/pym/portage/dbapi
	ginstall $(wildcard $(WORKSRC)/pym/portage/dbapi/*.py) \
		$(DESTDIR)$(portage_base)/pym/portage/dbapi
	ginstall -d $(DESTDIR)$(portage_base)/pym/portage/elog
	ginstall $(wildcard $(WORKSRC)/pym/portage/elog/*.py) \
		$(DESTDIR)$(portage_base)/pym/portage/elog
	ginstall -d $(DESTDIR)$(bindir_install)
	for x in ebuild emerge portageq repoman xpak; do \
		gln -s ../portage/bin/$${x} $(DESTDIR)$(bindir_install); \
	done
	ginstall -d $(DESTDIR)$(sbindir_install)
	for x in archive-conf dispatch-conf emaint emerge-webrsync env-update \
		etc-update fixpackages quickpkg regenworld; do \
		gln -s \
		  ..$(libdir_install)/portage/bin/$${x} \
		  $(DESTDIR)$(sbindir_install)/${x}; \
	done
	gln -s env-update $(DESTDIR)$(sbindir_install)/update-env
	gln -s etc-update $(DESTDIR)$(sbindir_install)/update-etc
	ginstall -d $(DESTDIR)/etc
	ginstall -d $(DESTDIR)/etc/portage
	touch $(DESTDIR)/etc/portage/.keep
