#!/usr/bin/env python
# vim:set sw=2 ts=2 sts=2:
# $Id$
#
# Tests for OpenCSW mirror identifying script.
# (C) 2009 Maciej Blizinski
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import mirror_check as mc
import re

class FooUnitTest(unittest.TestCase):
	def testUrlRE(self):
		urls = ["ftp://ftp.corbina.net/pub/Solaris/csw",
						"http://ftp.iforceready.it/pub/csw",
						"http://ftp.esat.net/mirrors/opencsw.org/csw/",
						"http://ftp.heanet.ie/pub/opencsw/",
						]
		url_re = re.compile(mc.URL_RE_STR)
		for url in urls:
			self.assertTrue(url_re.match(url),
					            "%s does not match %s" % (url, mc.URL_RE_STR))
	def testIsOpencswMirror(self):
		cmc = mc.OpencswMirrorChecker()
		urls = ["http://ftp.heanet.ie/pub/csw",
				    "http://ftp.heanet.ie/pub/opencsw/",
				    "http://ftp.heanet.ie/pub/blastwave.org/"]
		cmc.IdentifyUrls(urls)
		self.assertEqual(mc.URL_NOTFOUND, cmc.GetIdentification(urls[0]))
		self.assertEqual(mc.URL_OPENCSW, cmc.GetIdentification(urls[1]))
		self.assertEqual(mc.URL_BLASTWAVE, cmc.GetIdentification(urls[2]))


if __name__ == '__main__':
	unittest.main()
