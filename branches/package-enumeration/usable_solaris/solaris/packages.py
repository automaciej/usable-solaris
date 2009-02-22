import subprocess
import usable_solaris.packages.models as spm
import antlr3
import logging
import operator
logging.basicConfig(level=logging.DEBUG)

try:
    from pkginfoParser import pkginfoParser
    from pkginfoLexer import pkginfoLexer
except ImportError, e:
    logging.fata("You need to generate pkginfoParser and pkginfoLexer "
                 "using ANTLRv3.")
    raise


class MachineEnumerator(object):

    def __init__(self, fqdn):
        self.fqdn = fqdn
        self.ast = None

    def GetAst(self):
        if not self.ast:
            filename = "%s.pkginfo" % self.fqdn
            input_stream = open(filename, "r")
            char_stream = antlr3.ANTLRInputStream(input_stream)
            lexer = pkginfoLexer(char_stream)
            tokens = antlr3.CommonTokenStream(lexer)
            parser = pkginfoParser(tokens)
            self.ast = parser.pkginfo()
        return self.ast

    def Executify(self):
        ast = self.GetAst()
        self.PopulateDatabase(ast)

    def PopulateDatabase(self, ast):
        logging.debug("Populating database...")
        try:
            machine = spm.Machine.objects.get(fqdn=self.fqdn)
        except spm.Machine.DoesNotExist:
            machine = spm.Machine.objects.create(fqdn=self.fqdn)
            machine.save()
        for package in self.ast.tree.children:
            pkg_vars = {}
            for variable in package.children:
                var_name_ast, value_ast = variable.children
                var_name = var_name_ast.children[0].text
                value_list = [x.text for x in value_ast.children]
                var_value = reduce(operator.__add__, value_list)
                pkg_vars[var_name] = var_value
            if not machine.arch:
                machine.arch = pkg_vars['ARCH']
                machine.save()
            try:
                pkg = spm.Package.objects.get(pkginst=pkg_vars['PKGINST'])
            except spm.Package.DoesNotExist, e:
                pkg = spm.Package.objects.create(
                        pkginst=pkg_vars['PKGINST'],
                        name=pkg_vars['NAME'],
                        category=pkg_vars['CATEGORY'],
                        # email=pkg_vars['EMAIL'],
                        )
                pkg.save()
            try:
                pkg_ver = spm.PackageVersion.objects.get(
                        package=pkg,
                        version=pkg_vars['VERSION'])
            except spm.PackageVersion.DoesNotExist:
                pkg_ver = spm.PackageVersion.objects.create(
                        package=pkg,
                        version=pkg_vars['VERSION'])
                pkg_ver.save()
            try:
                pkg_inst = spm.PackageInstallation.objects.get(
                        machine=machine,
                        package_version=pkg_ver)
            except spm.PackageInstallation.DoesNotExist:
                pkg_inst = spm.PackageInstallation.objects.create(
                        machine=machine,
                        package_version=pkg_ver,
                        inst_date=pkg_vars['INSTDATE'],
                        status=pkg_vars['STATUS'],
                        )
                pkg_inst.save()




def main():
    machines = [
            'yaga.home.blizinski.pl',
            'vsol01.home.blizinski.pl',
            'lobelia.home.blizinski.pl',
            'unavailable.home.blizinski.pl',
    ]
    pe = MachineEnumerator(machines[0])
    pe.Executify()


if __name__ == "__main__":
    main()
