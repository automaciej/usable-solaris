# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
import usable_solaris.packages.models as pkgm
import logging

logging.basicConfig(level=logging.DEBUG)

def matrix(request):
    """Display a matrix of packages and hosts.

    This is clearly the slowest function in this code.
    """
    logging.debug("matrix() started")
    machines = pkgm.Machine.objects.all()
    package_versions = pkgm.PackageVersion.objects.all()
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
    return render_to_response("packages/matrix.html", {
        'package_versions': package_versions,
        'machines': machines,
        'matrix': table,
        })
