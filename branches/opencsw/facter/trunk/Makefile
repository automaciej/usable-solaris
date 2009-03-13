# Copyright 2009 Google Inc.
# Distributed under the terms of the GNU General Public License v2
# $Header: $

GARNAME = facter
GARVERSION = 1.5.4
CATEGORIES = server

DESCRIPTION = A library for retrieving facts from operating systems
define BLURB
  http://reductivelabs.com/products/facter/

  A cross-platform Ruby library for retrieving facts from operating systems.
  Supports multiple resolution mechanisms, any of which can be restricted to
  working only on certain operating systems or environments. Facter is
  especially useful for retrieving things like operating system names, IP
  addresses, MAC addresses, and SSH keys.

  It is easy to extend Facter to include your own custom facts or to include
  additional mechanisms for retrieving facts.
endef

MASTER_SITES = http://reductivelabs.com/downloads/facter/
DISTFILES  = $(GARNAME)-$(GARVERSION).tgz
DISTFILES += $(call admfiles,CSWfacter,)

# We define upstream file regex so we can be notifed of new upstream software
# release
UFILES_REGEX = $(GARNAME)-(\d+(?:\.\d+)*).tar.gz

CONFIGURE_SCRIPTS =
TEST_SCRIPTS =
BUILD_SCRIPTS =
INSTALL_SCRIPTS = custom
PREREQUISITE_PKGS = CSWcommon CSWruby


include gar/category.mk

install-custom:
	$(WORKSRC)/install.rb --destdir=$(DESTDIR)

install-custom-isa-sparcv8: install-custom

