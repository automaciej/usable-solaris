from django.contrib import admin
from usable_solaris.packages.models import Package, PackageVersion
from usable_solaris.packages.models import Machine, PackageInstallation

class PackageAdmin(admin.ModelAdmin):
    list_display = ('pkginst', 'category', 'name',
                    'vendor', 'email' , 'hotline')
admin.site.register(Package, PackageAdmin)

class PackageVersionAdmin(admin.ModelAdmin):
    list_display = ('package', 'version')
admin.site.register(PackageVersion, PackageVersionAdmin)

class MachineAdmin(admin.ModelAdmin):
    list_display = ('fqdn', 'arch')
admin.site.register(Machine, MachineAdmin)

class PackageInstallationAdmin(admin.ModelAdmin):
    list_display = ('package_version', 'machine', 'inst_date', 'status', 'arch')
admin.site.register(PackageInstallation, PackageInstallationAdmin)


