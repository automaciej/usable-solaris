from django.db import models

# Create your models here.

ARCH_CHOICES = (
        ('x86', 'Intel x86'),
        ('sparc', 'SPARC'),
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
    category = models.CharField(max_length=200)
    vendor = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    hotline = models.CharField(max_length=200)
    def __unicode__(self):
        return self.pkginst
    def get_absolute_url(self):
        return "/solaris/packages/%s/" % self.id
    class Meta:
        ordering = ['pkginst']


class PackageVersion(models.Model):
    package = models.ForeignKey(Package)
    version = models.CharField(max_length=200)
    def __unicode__(self):
        return "%s-%s" % (self.package, self.version)
    class Meta:
        ordering = ['package', 'version']
        unique_together = (('package', 'version'),)


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
        ordering = ['fqdn']


class PackageInstallation(models.Model):
    package_version = models.ForeignKey(PackageVersion)
    machine = models.ForeignKey(Machine)
    inst_date = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    arch = models.CharField(max_length=32)
    def __unicode__(self):
        return "%s on %s" % (self.package_version, self.machine)
    class Meta:
        ordering = ['machine', 'package_version']
        unique_together = (('package_version', 'machine'),)
