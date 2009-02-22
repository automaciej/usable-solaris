from django.contrib import admin
from usable_solaris.packages.models import Package, PackageVersion
from usable_solaris.packages.models import Machine, PackageInstallation

class PackageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Package, PackageAdmin)

class PackageVersionAdmin(admin.ModelAdmin):
    pass
admin.site.register(PackageVersion, PackageVersionAdmin)

class MachineAdmin(admin.ModelAdmin):
    pass
admin.site.register(Machine, MachineAdmin)

class PackageInstallationAdmin(admin.ModelAdmin):
    fields = ('package_version', 'machine')
admin.site.register(PackageInstallation, PackageInstallationAdmin)


