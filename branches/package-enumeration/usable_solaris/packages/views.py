# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
import usable_solaris.packages.models as pkgm
import logging

logging.basicConfig(level=logging.DEBUG)

def matrix(request, klass, template_path):
    """Display a matrix of packages and hosts.

    This is clearly the slowest function in this code.
    """
    logging.debug("matrix() started")
    machines = pkgm.Machine.objects.all()
    package_versions = klass.objects.all()
    package_installations = pkgm.PackageInstallation.objects.all()
    logging.debug("Created QuerySets")
    triplet_generator = (
            (x.machine.fqdn,
             x.package_version.package.pkginst,
             x.package_version.version)
            for x in package_installations)
    logging.debug("Generator done, creating the set.")
    package_installation_index = set(triplet_generator)
    logging.debug("Set ready. Generating table.")
    table = []
    for package_version in package_versions:
        row = {}
        row['package_version'] = package_version
        installation_list = []
        for machine in machines:
            triplet = (machine.fqdn,
                       package_version.package.pkginst,
                       package_version.version)
            installation_list.append(triplet in package_installation_index)
        row['package_installations'] = installation_list
        table.append(row)
    logging.debug("Table ready, returning.")
    return render_to_response(template_path, {
        'package_versions': package_versions,
        'machines': machines,
        'matrix': table,
        })

def package_matrix(request):
  return matrix(request, pkgm.PackageVersion, "packages/matrix.html")

def patch_matrix(request):
    """Display a matrix of packages and hosts.

    This is clearly the slowest function in this code.
    """
    logging.debug("matrix() started")
    machines = pkgm.Machine.objects.all()
    patches = pkgm.Patch.objects.all()
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
    for patch in patches:
        row = {}
        row['patch'] = patch
        installation_list = []
        for machine in machines:
            duplet = (machine.fqdn,
                      patch.name)
            installation_list.append(duplet in patch_installation_index)
        row['patch_installations'] = installation_list
        table.append(row)
    logging.debug("Table ready, returning.")
    return render_to_response("packages/patch_matrix.html", {
        'patches': patches,
        'machines': machines,
        'matrix': table,
        })

def old_packages(request):
  pkgs = []
  # for pkg in  pkgm.Package.objects.filter(pkginst__startswith="GOOG"):
  for pkg in  pkgm.Package.objects.all():
    pkg_data = {}
    # pkg = pkgm.Package.objects.get(pkginst="GOOGbackup-scripts")
    # Find the most popular installation of this package.
    versions = pkg.packageversion_set.all()
    versions_with_counts = [
        (x, x.packageinstallation_set.count())
        for x in versions]
    max_installations = max([x[1] for x in versions_with_counts])
    verss_with_max_installations = filter(lambda x: x[1] == max_installations,
                                         versions_with_counts)
    # There can be many of them, taking the first one.
    ver_with_max_installations = verss_with_max_installations[0][0]
    other_verss = filter(lambda x: x != ver_with_max_installations,
                         versions)
    debug = other_verss
    pkg_data['pkg'] = pkg
    pkg_data['other_verss'] = other_verss
    pkg_data['popular_ver'] = ver_with_max_installations
    pkg_data['popular_count'] = max_installations
    pkg_data['package_ok'] = len(other_verss) == 0
    pkgs.append(pkg_data)
  return render_to_response("packages/old_packages.html", {
    'packages': pkgs,
    'debug': debug,
    })

def not_installed(request, object_id):
  pkg = pkgm.Package.objects.get(pk=object_id)
  # Find all the machines on which any version of the package isn't installed
  pkg_versions = pkg.packageversion_set.all()
  machines = pkgm.Machine.objects.exclude(
      packageinstallation__package_version__package__id=object_id)
  return render_to_response("packages/not_installed.html", {
    'object': pkg,
    'machines': machines,
    })

def index(request):
  return render_to_response("packages/index.html")
