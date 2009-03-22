#!/usr/bin/env python
# vim:set sw=2 ts=2 sts=2:
# $Id$
#
# Identifies OpenCSW mirror status.
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

import urllib2
import re
import threading
import logging

logging.basicConfig(level=logging.DEBUG)

MIRRORS_URL = "http://www.opencsw.org/mirrors"
URL_RE_STR = r"^(?P<url>(ht|f)tp://\w+(\.\w+)*.*)$"
URL_OPENCSW, URL_BLASTWAVE, URL_UNKNOWN, URL_NOTFOUND = (
		"OpenCSW", "Blastwave", "Unknown", "Not found")

NOCHECK_URLS = set([
	"http://www.w3.org/TR/html4/loose.dtd",
	"http://css.maxdesign.com.au/listamatic/index.htm",
	"http://www.canoedissent.org.uk/mirror/status/",
	"http://pkgutil.wikidot.com/",
	"http://www.bolthole.com/solaris/pkg-get.html",
	"http://ftp.math.purdue.edu/mirrors/opencsw.org/wget.i386", ])


class OpencswMirrorChecker(object):

	url_re = re.compile(URL_RE_STR)

	def __init__(self):
		self.urls_by_identification = {}
		self.identifications_by_url = {}

	def ExtractUrls(self, html):
		for word in re.split(r'(<|>|"|=|\s+)', html):
			if self.url_re.search(word):
				yield word

	def GetUrls(self):
		url_d = urllib2.urlopen(MIRRORS_URL)
		mirrors_html = url_d.read()
		return self.ExtractUrls(mirrors_html)

	def IdentifyUrls(self, urls):

		class UrlIdentifier(threading.Thread):
			
			def __init__(self, url, callback):
				super(UrlIdentifier, self).__init__()
				self.url = url
				self.callback = callback

			def run(self):
				result = URL_UNKNOWN
				try:
					if self.url.endswith("/"):
						sep = ""
					else:
						sep = "/"
					readme_url = self.url + sep + "README"
					logging.debug("Opening %s" % (readme_url))
					url_d = urllib2.urlopen(readme_url, None, 30)
					html = url_d.read()
					logging.debug("%s length: %s" % (readme_url, len(html)))
					if re.search(r'blastwave', html, flags=re.I):
						result = URL_BLASTWAVE
					if re.search(r'opencsw', html, flags=re.I):
						result = URL_OPENCSW
					else:
						logging.debug("Unknown %s" % (readme_url))
				except urllib2.HTTPError:
					result = URL_NOTFOUND
				except urllib2.URLError:
					result = URL_NOTFOUND
				finally:
					logging.debug("Calling back to report '%s' with '%s'" % (result, self.url))
					self.callback(self.url, result)

		url_fetchers = []
		logging.info("Spawning fetchers.")
		for url in urls:
			if url in NOCHECK_URLS:
				continue
			t = UrlIdentifier(url, self.CollectData)
			t.start()
			url_fetchers.append(t)
		logging.info("Waiting for fetchers.")
		for t in url_fetchers:
			t.join()

	def CollectData(self, url, result):
		if not result in self.urls_by_identification:
			self.urls_by_identification[result] = []
		self.urls_by_identification[result].append(url)
		self.identifications_by_url[url] = result

	def GetIdentification(self, url):
		return self.identifications_by_url[url]

	def PrintIdentification(self):
		for site_id, url_list in self.urls_by_identification.iteritems():
			print "%s:" % site_id
			for url in sorted(url_list):
				print "    %s" % url

	def Run(self):
		urls = self.GetUrls()
		self.IdentifyUrls(urls)
		self.PrintIdentification()


def main():
	cmc = OpencswMirrorChecker()
	cmc.Run()


if __name__ == '__main__':
	main()
