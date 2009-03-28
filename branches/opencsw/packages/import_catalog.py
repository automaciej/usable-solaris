#!/usr/bin/python
# vim:set sw=2 ts=2 sts=2:
#
# $Id$
#

import antlr3
import logging
import urllib2

logging.basicConfig(level=logging.DEBUG)

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
      logging.debug("Downloading the catalog from the web")
      catalog_url_d = urllib2.urlopen(
          "http://ftp.heanet.ie/pub/opencsw/current/i386/5.10/catalog")
      logging.debug("Creating intermediate objects")
      char_stream = antlr3.ANTLRInputStream(catalog_url_d)
      lexer = catalogLexer(char_stream)
      tokens = antlr3.CommonTokenStream(lexer)
      parser = catalogParser(tokens)
      logging.debug("Parsing...")
      self.ast = parser.catalog()
      logging.debug("Parsing done.")
    return self.ast


if __name__ == "__main__":
  ci = CatalogImporter()
  ast = ci.GetAst()
