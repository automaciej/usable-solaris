// Grammar for Solaris showrev -p command.
// $Id$

grammar showrev;

options {
  language=Python;
  output=AST;
  ASTLabelType=CommonTree;
}

tokens {
	TOK_PATCH;
	TOK_PACKAGE;
}

WS	:	' ';
NEWLINE	:	'\n';
COLON	:	':';
KW_PATCH	:	'Patch';
KW_OBSOLETES
	:	'Obsoletes';
KW_REQUIRES
	:	'Requires';
KW_INCOMPATIBLES
	:	'Incompatibles';
KW_PACKAGES
	:	'Packages';
PATCH_NUMBER
	:	'0'..'9'+ '-' '0'..'9' '0'..'9';
PACKAGE_NAME
	:	('a'..'z'|'A'..'Z'|'0'..'9'|'-')+;
showrev_line
	:	KW_PATCH COLON WS
		PATCH_NUMBER WS
		obsoletes WS
		requires WS 
		incompatibles WS
		packages WS?
		NEWLINE
		-> ^(TOK_PATCH PATCH_NUMBER
		  obsoletes
		  requires
		  incompatibles
		  packages
		)
	;
	
obsoletes
	:	KW_OBSOLETES COLON WS patch_list? -> ^(KW_OBSOLETES patch_list?)

	;
	
requires
	:	KW_REQUIRES COLON WS patch_list? -> ^(KW_REQUIRES patch_list?)
	;
incompatibles
	:	KW_INCOMPATIBLES COLON WS patch_list? -> ^(KW_INCOMPATIBLES patch_list?)
	;
packages:	KW_PACKAGES COLON WS package_list? -> ^(KW_PACKAGES package_list?)
	;

patch_list
	:	PATCH_NUMBER (patch_list_continuation_elem)*
	;
patch_list_continuation_elem
	:	',' WS PATCH_NUMBER -> PATCH_NUMBER;
package_list
	:	PACKAGE_NAME (package_list_continuation_elem)*
	;
package_list_continuation_elem
	:	',' WS PACKAGE_NAME -> PACKAGE_NAME;
showrev	:	showrev_line+;
