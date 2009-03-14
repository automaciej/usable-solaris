# Copyright 2009 Google Inc.
# Distributed under the terms of the GNU General Public License v2
# $Header: $

GARNAME = puppet
GARVERSION = 0.24.7
CATEGORIES = server

DESCRIPTION = A configuration management solution.
define BLURB
  http://reductivelabs.com/products/puppet/

  The Puppet framework provides a means to describe IT infrastructure as policy,
  execute that policy to build services then audit and enforce ongoing changes
  to the policy.

  Puppet helps accomplish the goal of a hands-off, automated infrastructure.
endef

MASTER_SITES = http://reductivelabs.com/downloads/puppet/
DISTFILES  = $(GARNAME)-$(GARVERSION).tgz
DISTFILES += $(call admfiles,CSWpuppet,)
DISTFILES += csw$(GARNAME) csw$(GARNAME).xml svc-puppetd
DISTFILES += puppet.conf.CSW

# We define upstream file regex so we can be notifed of new upstream software
# release
UFILES_REGEX = $(GARNAME)-(\d+(?:\.\d+)*).tar.gz

SPKG_CLASSES = none cswinitsmf

CONFIGURE_SCRIPTS =
TEST_SCRIPTS =
BUILD_SCRIPTS =
INSTALL_SCRIPTS = custom
PREREQUISITE_PKGS = CSWcommon CSWruby


include gar/category.mk

install-custom:
	(cd $(WORKSRC); ./install.rb --destdir=$(DESTDIR))
