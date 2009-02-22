grammar pkginfo;

options {
  language=Python;
  output=AST;
  ASTLabelType=CommonTree;
}

tokens {
	PACKAGE;
	VARIABLE;
	VARIABLE_NAME;
	VALUE;
}

COLON	:	':';
WS	:	' '+;
NEWLINE :	'\n';
UPPERCASEWORD
	:	('A'..'Z')+;
ANYTHING
	:	.;

stuff	:	(UPPERCASEWORD|COLON|WS|ANYTHING)+;
variable_line
	:	WS? varname COLON WS stuff NEWLINE -> ^(VARIABLE ^(VARIABLE_NAME varname) ^(VALUE stuff));
stuff_line
	:	stuff NEWLINE -> ^(VALUE stuff);
pkgparam_line
	:	variable_line
	|	stuff_line -> ;
solaris_package
	:	pkgparam_line+ NEWLINE -> ^(PACKAGE pkgparam_line+);
pkginfo	:	solaris_package+;
varname	:	UPPERCASEWORD;
