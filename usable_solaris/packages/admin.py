from django.contrib import admin
from usable_solaris.packages.models import Package, PackageVersion, Patch
from usable_solaris.packages.models import PatchRevision
from usable_solaris.packages.models import Machine, PackageInstallation
from usable_solaris.packages.models import PatchInstallation

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

class PatchAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patch, PatchAdmin)

class PatchRevisionAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatchRevision, PatchRevisionAdmin)

class PackageInstallationAdmin(admin.ModelAdmin):
    list_display = ('package_version', 'machine', 'inst_date', 'status', 'arch')
admin.site.register(PackageInstallation, PackageInstallationAdmin)

class PatchInstallationAdmin(admin.ModelAdmin):
    list_display = ('patch_revision', 'machine')
admin.site.register(PatchInstallation, PatchInstallationAdmin)
