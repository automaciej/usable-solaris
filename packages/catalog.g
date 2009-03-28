grammar catalog;

options {
  language=Python;
  output=AST;
  ASTLabelType=CommonTree;
}

tokens {
  PACKAGE;
  PACKAGE_NAME;
  VERSION;
  SOFT_VERSION;
  PKG_REVISION;
  PKGINST;
  MD5SUM;
  DEPENDENCIES;
  FILENAME;
  LENGTH;
}

HEADER	:	'-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA1\n\n';
FOOTER	:	'-----BEGIN PGP SIGNATURE-----' .* '-----END PGP SIGNATURE-----';
COMMENT_LINE	:	'#' (~('\n'))* '\n';
NL	:	'\n';
WS	:	' ';
COMMA	:	',';
NON_COMMA
	:	(~(' '|'\n'|'|'|','))+;
catalog	:	header
		comment_block?
		package_line+
		footer
		-> package_line+
		;
comment_block
	:	COMMENT_LINE+;
		
package_line
	:	pkgname WS
		version WS
		pkginst WS
		filename WS
		md5sum WS
		length WS
		pkginst_list WS
		class_r
		(WS class_r)*
		'\n'
		-> ^(PACKAGE pkgname version pkginst filename md5sum length pkginst_list)
		;
pkginst_list
	:	pkginst ('|' pkginst)* -> ^(DEPENDENCIES pkginst (pkginst)*)
	;
pkginst	:	word -> ^(PKGINST word)
	;
word	:	NON_COMMA
	;
class_r	:	'none'|'user'
	;
header	:	HEADER;
footer	:	FOOTER;
pkgname	:	word -> ^(PACKAGE_NAME word);
filename:	filename_literal -> ^(FILENAME filename_literal);
filename_literal
	:	(NON_COMMA|COMMA)+;
version	:	soft_version (COMMA 'REV=' pkg_revision)? -> ^(VERSION soft_version pkg_revision?);
soft_version
	:	word -> ^(SOFT_VERSION word);
pkg_revision
	:	word -> ^(PKG_REVISION word);
length	:	word -> ^(LENGTH word);
md5sum	:	word -> ^(MD5SUM word);
