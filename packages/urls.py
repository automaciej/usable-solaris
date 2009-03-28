from django.conf.urls.defaults import *

urlpatterns = patterns('',
        # ('^$', 'opencsw.packages.views.index')
        (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'packages/index.html'}),
)
