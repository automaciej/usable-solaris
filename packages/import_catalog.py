#!/usr/bin/python
# vim:set sw=2 ts=2 sts=2:
#
# $Id$
#

import antlr3
import logging
import urllib2

try:
  from catalogParser import catalogParser
  from catalogLexer import catalogLexer
except ImportError, e:
  logging.fatal("You need to generate parsers and lexers "
                "using ANTLRv3.\nYou can use GNU make.")
  raise

class CatalogImporter(object):

  def __init__(self):
    self.ast = None

  def GetAst(self):
    if not self.ast:
      catalog_url_d = urllib2.urlopen(
          "http://ftp.heanet.ie/pub/opencsw/current/i386/5.10/catalog")
      char_stream = antlr3.ANTLRInputStream(catalog_url_d)
      lexer = catalogLexer(char_stream)
      tokens = antlr3.CommonTokenStream(lexer)
      parser = catalogParser(tokens)
      self.ast = parser.catalog()
    return self.ast


if __name__ == "__main__":
    print "Please use classes defined in this package."
