# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
import usable_solaris.packages.models as pkgm
import logging

logging.basicConfig(level=logging.DEBUG)

def package_matrix(request):
    """Display a matrix of packages and hosts."""
    logging.debug("package_matrix() started")
    machines = pkgm.Machine.objects.order_by('fqdn')
    package_versions = pkgm.PackageVersion.objects.order_by(
            'package__pkginst',
            'version')
    package_installations = pkgm.PackageInstallation.objects.order_by(
        'package_version__package__pkginst',
        'package_version__version',
        'machine__fqdn')
    logging.debug("Generating table.")
    table = []
    pkg_inst_pos = 0
    pkg_inst_pos_max = len(package_installations) - 1
    for package_version in package_versions:
        row = {}
        row['package_version'] = package_version
        installation_list = []
        for machine in machines:
            pkg_inst = package_installations[pkg_inst_pos]
            if (machine.id == pkg_inst.machine.id and
                    pkg_inst.package_version.id == package_version.id):
                installation_list.append(True)
                if pkg_inst_pos < pkg_inst_pos_max:
                    pkg_inst_pos += 1
            else:
                installation_list.append(False)
        row['package_installations'] = installation_list
        table.append(row)
    logging.debug("Table ready, returning.")
    return render_to_response("packages/matrix.html", {
        'package_versions': package_versions,
        'machines': machines,
        'matrix': table
    })

def patch_matrix(request):
    """Display a matrix of patches and hosts."""
    machines = pkgm.Machine.objects.order_by("fqdn")
    patches = pkgm.Patch.objects.order_by("name")
    patch_installations = pkgm.PatchInstallation.objects.order_by(
            "patch__name", "machine__fqdn")
    logging.debug("Generating table.")
    table = []
    patch_inst_pos = 0
    patch_inst_pos_max = len(patch_installations) - 1
    for patch in patches:
        row = {}
        row['patch'] = patch
        installation_list = []
        for machine in machines:
            patch_inst = patch_installations[patch_inst_pos]
            if (machine.id == patch_inst.machine.id and
                    patch_inst.patch.id == patch.id):
                installation_list.append(True)
                if patch_inst_pos < patch_inst_pos_max:
                    patch_inst_pos += 1
            else:
                installation_list.append(False)
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
  for pkg in  pkgm.Package.objects.all():
    pkg_data = {}
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
    other_verss = filter(lambda x: x.packageinstallation_set.count() > 0,
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

def package_report(request):
  packages = pkgm.Package.objects.all()
  def GetDict(package):
    versions = package.packageversion_set.all()
    installation_counts = [version.packageinstallation_set.count()
                           for version in versions]
    installations_count = sum(installation_counts)
    machines = pkgm.Machine.objects.filter(
        packageinstallation__package_version__package__id=package.id)
    except_machines = pkgm.Machine.objects.exclude(id__in=[x.id
                                                           for x in machines])
    return {
        'package': package,
        'versions': versions,
        'installations_count': installations_count,
        'machines': machines,
        'except_machines': except_machines,
        'print_machines': len(machines) < 10 and len(machines) > 0,
        'print_except_machines': (len(except_machines) < 10
                                  and len(except_machines) > 0),
    }
  dicts_with_packages = [GetDict(x) for x in packages]
  # By the number of installations
  by_installation_count = {}
  for pkg_dict in dicts_with_packages:
    if pkg_dict['installations_count'] not in by_installation_count:
      by_installation_count[pkg_dict['installations_count']] = []
    by_installation_count[pkg_dict['installations_count']].append(pkg_dict)
  return render_to_response("packages/package_report.html", {
    'dicts_with_packages': dicts_with_packages,
    'by_installation_count': reversed(by_installation_count.items()),
  })

def index(request):
  return render_to_response("packages/index.html")
