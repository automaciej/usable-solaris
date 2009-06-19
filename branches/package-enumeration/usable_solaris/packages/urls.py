from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
# from django.views.generic.list_detail import object_detail
from usable_solaris.packages.models import Machine
from usable_solaris.packages.models import Package
from usable_solaris.packages.models import Patch
from usable_solaris.packages.models import PatchRevision
import usable_solaris.packages.views

urlpatterns = patterns('',
    (r'^machines/$', 'django.views.generic.list_detail.object_list',
        { 'queryset': Machine.objects.all()}),
    (r'^machines/(?P<object_id>[0-9]+)/$',
        'django.views.generic.list_detail.object_detail',
        { 'queryset': Machine.objects.all()}),
    (r'^machines/(?P<object_id>[0-9]+)/long/$',
        'django.views.generic.list_detail.object_detail',
        { 'queryset': Machine.objects.all(),
          'template_name': 'packages/machine_detail_long.html'}),
    (r'^packages/$', 'django.views.generic.list_detail.object_list',
        { 'queryset': Package.objects.all()}),
    (r'^packages/(?P<slug>[-\w]+)/$',
        'django.views.generic.list_detail.object_detail',
        { 'queryset': Package.objects.all()}),
    (r'^patches/$', 'django.views.generic.list_detail.object_list',
        { 'queryset': Patch.objects.all()}),
    (r'^patches/(?P<slug>\d+)/$',
        'django.views.generic.list_detail.object_detail',
        { 'queryset': Patch.objects.all()}),
    (r'^patches/(?P<slug>\d+-\d+)/$',
        'django.views.generic.list_detail.object_detail',
        { 'queryset': PatchRevision.objects.all()}),
    (r'^package-matrix/$', 'usable_solaris.packages.views.package_matrix'),
    (r'^patch-matrix/$', 'usable_solaris.packages.views.patch_matrix'),
    (r'^old-packages/$', 'usable_solaris.packages.views.old_packages'),
    (r'^package-report/$', 'usable_solaris.packages.views.package_report'),
    (r'^not-installed/(?P<object_id>[0-9]+)/$', 'usable_solaris.packages.'
                                                'views.not_installed'),
    (r'^$', 'usable_solaris.packages.views.index'),
)
