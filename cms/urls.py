from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^frontend-media/(?P<path>.*)$', 'django.views.static.serve',
                        { 'document_root': '/home/smudge/work/django-practice/cms/media/' }),
                       (r'^tiny_mce/(?P<path>.*)$', 'django.views.static.serve',
                        { 'document_root': '/home/smudge/work/django-practice/cms/scripts/tiny_mce/' }),
                       (r'^search/$', 'cms.search.views.search'),
                       (r'^comments/', include('django.contrib.comments.urls')),
                       (r'^weblog/categories/', include('coltrane.urls.categories')),
                       (r'^weblog/links/', include('coltrane.urls.links')),
                       (r'^weblog/tags/', include('coltrane.urls.tags')),    
                       (r'^weblog/', include('coltrane.urls.entries')),    
                       (r'', include('django.contrib.flatpages.urls')),
)
