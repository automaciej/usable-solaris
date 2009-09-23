from django.db import models

# Create your models here.

ARCH_CHOICES = (
        ("x86", "Intel x86"),
        ("sparc", "SPARC"),
)

class Package(models.Model):
    """Solaris package.

    Example data:

   PKGINST:  CSWapache2rt
      NAME:  apache2rt - Apache 2.2 runtime libraries
  CATEGORY:  application
      ARCH:  sparc
   VERSION:  2.2.6,REV=2007.10.25
   BASEDIR:  /
    VENDOR:  http://httpd.apache.org/ packaged for CSW by Cory Omand
    PSTAMP:  comand@ra-20071025012647
  INSTDATE:  Feb 21 2009 01:18
   HOTLINE:  http://www.blastwave.org/bugtrack/
     EMAIL:  comand@blastwave.org
    STATUS:  completely installed
     FILES:       22 installed pathnames

    """
    pkginst = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=200)
    vendor = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    hotline = models.CharField(max_length=200)
    def __unicode__(self):
        return self.pkginst
    def get_absolute_url(self):
        return "/solaris/packages/%s/" % self.slug
    def not_installed_on_machines(self):
        # Find all the machines on which any version of the package isn't installed
        pkg_versions = self.packageversion_set.all()
        machines = Machine.objects.exclude(
            packageinstallation__package_version__package__id=self.id)
        return  machines
    class Meta:
        ordering = ["pkginst"]


class PackageVersion(models.Model):
    package = models.ForeignKey(Package)
    version = models.CharField(max_length=200)
    def other_package_versions(self):
        return self.package.packageversion_set.exclude(id=self.id)
    def machines_with_other_versions(self):
        return Machine.objects.filter(
            packageinstallation__package_version__in=self.package.packageversion_set.exclude(id=self.id))
    def __unicode__(self):
        return "%s-%s" % (self.package, self.version)
    class Meta:
        ordering = ["package", "version"]
        unique_together = (("package", "version"),)


class Machine(models.Model):
    fqdn = models.CharField(max_length=200)
    arch = models.CharField(max_length=32)
    def __unicode__(self):
        return self.fqdn
    def get_absolute_url(self):
        return "/solaris/machines/%s/" % self.id
    def short(self):
        return unicode(self.fqdn).split(".")[0]
    class Meta:
        ordering = ["fqdn"]


class PackageInstallation(models.Model):
    package_version = models.ForeignKey(PackageVersion)
    machine = models.ForeignKey(Machine)
    inst_date = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    arch = models.CharField(max_length=32)
    def machines_with_the_same_version(self):
        return self.package_version.packageinstallation_set.all()
    def status_summary(self):
        """Returns a dict with more information about the installation."""
        d = {}
        all_machines = Machine.objects.all()
        machines_same_version = self.machines_with_the_same_version()
        machines_with_other_versions = self.package_version.machines_with_other_versions()
        d['machines_with_other_versions'] = machines_with_other_versions
        d['all_machines'] = all_machines
        d['not_popular'] = (len(machines_with_other_versions) > len(machines_same_version))
        d['no_other_versions'] = (len(machines_with_other_versions) == 0)
        return d
    def __unicode__(self):
        return "%s on %s" % (self.package_version, self.machine)
    class Meta:
        ordering = ["machine", "package_version"]
        unique_together = (("package_version", "machine"),)


class Patch(models.Model):
    number_1 = models.IntegerField(unique=True)
    slug = models.SlugField(unique=True)
    def __unicode__(self):
        return u"%s" % self.number_1
    def get_absolute_url(self):
        return "/solaris/patches/%s/" % self.number_1
    class Meta:
        ordering = ["number_1"]
        verbose_name_plural = "patches"

class PatchRevision(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    patch = models.ForeignKey(Patch)
    number_2 = models.IntegerField()
    obsoletes = models.ManyToManyField(
        "self", related_name="obsoleted_by",
        null=True, blank=True, symmetrical=False)
    requires = models.ManyToManyField(
        "self", related_name="required_by", null=True, blank=True,
        symmetrical=False)
    incompatibles = models.ManyToManyField(
        "self", null=True, blank=True, symmetrical=False)
    packages = models.ManyToManyField(Package, null=True, blank=True)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/solaris/patches/%s/" % self.slug
    class Meta:
        ordering = ["patch", "number_2"]
        verbose_name_plural = "patches"

class PatchInstallation(models.Model):
    patch_revision = models.ForeignKey(PatchRevision)
    machine = models.ForeignKey(Machine)
    def __unicode__(self):
      return u"%s on %s" % (self.patch, self.machine)
