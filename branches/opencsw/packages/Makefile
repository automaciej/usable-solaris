# Rules for generating parsers and lexers.
# $Id: Makefile 18 2009-02-24 08:06:18Z maciej.blizinski $

all: catalog-grammar

ANTLR=antlr-3.1.1

%-grammar: $(ANTLR).jar %-antlr

%-antlr: %.g
	java -classpath $(ANTLR).jar org.antlr.Tool $<

$(ANTLR).jar:
	wget http://www.antlr.org/download/$(ANTLR).jar
