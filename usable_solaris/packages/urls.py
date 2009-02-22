from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
# from django.views.generic.list_detail import object_detail
from usable_solaris.packages.models import Machine
from usable_solaris.packages.models import Package

urlpatterns = patterns('',
    (r'^machines/$', 'django.views.generic.list_detail.object_list',
        { 'queryset': Machine.objects.all()}),
    (r'^machines/(?P<object_id>[0-9]+)/$',
        'django.views.generic.list_detail.object_detail',
        { 'queryset': Machine.objects.all()}),
    (r'^packages/$', 'django.views.generic.list_detail.object_list',
        { 'queryset': Package.objects.all()}),
    (r'^packages/(?P<object_id>[0-9]+)/$',
        'django.views.generic.list_detail.object_detail',
        { 'queryset': Package.objects.all()}),
)
