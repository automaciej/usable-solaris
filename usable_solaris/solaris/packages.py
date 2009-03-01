import antlr3
import logging
import operator
import subprocess
import usable_solaris.packages.models as pkgm

logging.basicConfig(level=logging.DEBUG)

try:
  from pkginfoParser import pkginfoParser
  from pkginfoLexer import pkginfoLexer
  from showrevParser import showrevParser
  from showrevLexer import showrevLexer
except ImportError, e:
  logging.fatal("You need to generate parsers and lexers "
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
    machine, _ = pkgm.Machine.objects.get_or_create(fqdn=self.fqdn)
    package_installation_ids = set()
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
      pkg, _ = pkgm.Package.objects.get_or_create(
          pkginst=pkg_vars['PKGINST'],
          defaults={
              'name': pkg_vars['NAME'],
              'category': pkg_vars['CATEGORY'],
              'slug': pkg_vars['PKGINST'],
          })
      pkg_ver, _ = pkgm.PackageVersion.objects.get_or_create(
          package=pkg,
          version=pkg_vars['VERSION'])
      try:
        pkg_inst = pkgm.PackageInstallation.objects.get(
                machine=machine,
                package_version=pkg_ver)
      except pkgm.PackageInstallation.DoesNotExist:
        if 'INSTDATE' in pkg_vars:
          inst_date = pkg_vars['INSTDATE']
        else:
          inst_date = ""
        pkg_inst = pkgm.PackageInstallation.objects.create(
            machine=machine,
            package_version=pkg_ver,
            inst_date=inst_date,
            status=pkg_vars['STATUS'])
        pkg_inst.save()
      package_installation_ids.add(pkg_inst.id)
    # Remove old installations
    installations_in_db = pkgm.PackageInstallation.objects.filter(
        machine__fqdn=self.fqdn)
    for package_installation in installations_in_db:
      if package_installation.id not in package_installation_ids:
        logging.debug("Removing package installation: "
            "'%s'" % package_installation)
        package_installation.delete()


class DatabasePopulator(object):

  def ReadMachines(self, filename):
    self.machines = [x.strip() for x in open(filename, "r").readlines()]

  def DoMachines(self, machines):
    for fqdn in machines:
      logging.debug("packages of %s..." % fqdn)
      me = MachineEnumerator(fqdn)
      me.Executify()
      logging.debug("patches of %s..." % fqdn)
      pe = PatchEnumerator(fqdn)
      pe.PopulateDatabase()

  def ProcessFile(self, filename):
    self.ReadMachines(filename)
    self.DoMachines(self.machines)


class PatchEnumerator(object):

  def __init__(self, fqdn):
    self.fqdn = fqdn
    self.ast = None

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
    machine, _ = pkgm.Machine.objects.get_or_create(fqdn=self.fqdn)
    for patch_ast in tree.children:
      # [u'125096-15',
      #  u'Obsoletes',
      #  u'Requires',
      #  u'Incompatibles',
      #  u'Packages']
      try:
        patch_name = patch_ast.children[0].text
        obsoletes_ast = patch_ast.children[1]
        requires_ast = patch_ast.children[2]
        incompatibles_ast = patch_ast.children[3]
        packages_ast = patch_ast.children[4]
      except IndexError, e:
        logging.warn(e)
        continue
      number_1, number_2 = [int(x) for x in patch_name.split("-")]
      patch, _ = pkgm.Patch.objects.get_or_create(name=patch_name,
              defaults={
                  'number_1': number_1,
                  'number_2': number_2,
                  'slug': patch_name, })
      patch_installation, _ = pkgm.PatchInstallation.objects.get_or_create(
                  patch=patch, machine=machine)
      # Packages
      for package_ast in packages_ast.children:
        pkginst = package_ast.text
        pkg = pkgm.Package.objects.get(pkginst=pkginst)
        patch.packages.add(pkg)
      # Obsoleted patches
      for obsoleted_patch_ast in obsoletes_ast.children:
        obsoleted_patch_name = obsoleted_patch_ast.text
        number_1, number_2 = [int(x)
                              for x in obsoleted_patch_name.split("-")]
        obsoleted_patch, _ = pkgm.Patch.objects.get_or_create(
            name=obsoleted_patch_name, defaults={
              'number_1': number_1,
              'number_2': number_2,
              'slug': obsoleted_patch_name, })
        patch.obsoletes.add(obsoleted_patch)
      for required_patch_ast in requires_ast.children:
        required_patch_name = required_patch_ast.text
        number_1, number_2 = [int(x)
                              for x in required_patch_name.split("-")]
        required_patch, _ = pkgm.Patch.objects.get_or_create(
            name=required_patch_name, defaults={
                  'number_1': number_1,
                  'number_2': number_2,
                  'slug': required_patch_name, })
        patch.requires.add(required_patch)


class ConexpWriter(object):

  def GeneratePatchMatrixCxt(self):
    """Produces conexp format.

    http://conexp.sf.net/
    """
    output = ["B\n\n"]
    logging.debug("GeneratePatchMatrixCxt() started")
    machines = pkgm.Machine.objects.all()
    output.append("%s\n" % len(machines))
    patches = pkgm.Patch.objects.all()
    output.append("%s\n" % len(patches))
    output.append("\n")
    for machine in machines:
      output.append("%s\n" % machine)
    for patch in patches:
      output.append("%s\n" % patch)
    patch_installations = pkgm.PatchInstallation.objects.all()
    logging.debug("Created QuerySets")
    duplet_generator = (
            (x.machine.fqdn,
             x.patch.name)
            for x in patch_installations)
    logging.debug("Generator done, creating the set.")
    patch_installation_index = set(duplet_generator)
    logging.debug("Set ready. Generating table.")
    table = []
    for machine in machines:
      for patch in patches:
        duplet = (machine.fqdn,
                  patch.name)
        if duplet in patch_installation_index:
          output.append("X")
        else:
          output.append(".")
      output.append("\n")
    return "".join(output)


def main():
    print "Please use package classes."


if __name__ == "__main__":
    main()
