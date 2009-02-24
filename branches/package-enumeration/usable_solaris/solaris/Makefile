# Rules for generating parsers and lexers.
# $Id$

all: showrev pkginfo

ANTLR=antlr-3.1.1

showrev: $(ANTLR).jar showrev.g
	java -classpath $(ANTLR).jar org.antlr.Tool showrev.g

pkginfo: $(ANTLR).jar pkginfo.g
	java -classpath $(ANTLR).jar org.antlr.Tool pkginfo.g

$(ANTLR).jar:
	wget http://www.antlr.org/download/$(ANTLR).jar
