import antlr3
import logging
import operator
import subprocess
import usable_solaris.packages.models as spm

logging.basicConfig(level=logging.DEBUG)

try:
    from pkginfoParser import pkginfoParser
    from pkginfoLexer import pkginfoLexer
    from showrevParser import showrevParser
    from showrevLexer import showrevLexer
except ImportError, e:
    logging.fata("You need to generate parsers and lexers "
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
        """Method name inspired by Stevey Yegge.

        The Verb "execute", and its synonymous cousins "run", "start", "go",
        "justDoIt", "makeItSo", and the like, can perform the work of any other
        Verb by replacing it with an appropriate Executioner and a call to
        execute(). Need to wait? Waiter.execute(). Brush your teeth?
        ToothBrusher(myTeeth).go(). Take out the garbage?
        TrashDisposalPlanExecutor.doIt().

        http://tinyurl.com/kxubn
        """
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


class PatchEnumerator(object):

    def __init__(self, fqdn):
        self.fqdn = fqdn
        self.ast = None

    def run(self):
        ast = self.GetAst()

    def GetAst(self):
        if not self.ast:
            filename = "%s.showrev" % self.fqdn
            input_stream = open(filename, "r")
            char_stream = antlr3.ANTLRInputStream(input_stream)
            lexer = showrevLexer(char_stream)
            tokens = antlr3.CommonTokenStream(lexer)
            parser = showrevParser(tokens)
            self.ast = parser.showrev()
        return self.ast

    def PopulateDatabase(self):
        ast = self.GetAst()
        tree = ast.tree
        machine, machine_created = spm.Machine.objects.get_or_create(fqdn=self.fqdn)
        for patch_ast in tree.children:
            # [u'125096-15', u'Obsoletes', u'Requires', u'Incompatibles',
            #         u'Packages']
            patch_name = patch_ast.children[0].text
            obsoletes_ast = patch_ast.children[1]
            requires_ast = patch_ast.children[2]
            incompatibles_ast = patch_ast.children[3]
            packages_ast = patch_ast.children[4]
            number_1, number_2 = [int(x) for x in patch_name.split("-")]
            patch, patch_created = spm.Patch.objects.get_or_create(name=patch_name,
                    defaults={
                        'number_1': number_1,
                        'number_2': number_2,
                        })
            try:
                patch_installation = spm.PatchInstallation.objects.get(
                        patch=patch, machine=machine)
            except spm.PatchInstallation.DoesNotExist:
                patch_installation = spm.PatchInstallation.objects.create(
                        patch=patch, machine=machine)



def main():
    machines = [
            'yaga.home.blizinski.pl',
            'vsol01.home.blizinski.pl',
            'lobelia.home.blizinski.pl',
            # 'unavailable.home.blizinski.pl',
    ]
    for machine in machines:
        me = MachineEnumerator(machines)
        me.Executify()


if __name__ == "__main__":
    main()
