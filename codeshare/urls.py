from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^frontend-media/(?P<path>.*)$', 'django.views.static.serve',
                        { 'document_root': '/home/smudge/work/django-practice/codeshare/templates/media/' }),
                       (r'^snippets/', include('cab.urls.snippets')),
                       (r'^languages/', include('cab.urls.languages')),
                       )
