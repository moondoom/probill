from django.conf.urls.defaults import patterns, include, url
import settings
import moon

from django.contrib import admin
admin.autodiscover()
moon.autodiscover()

urlpatterns = patterns('',
    url(r'^client/',include('billing.urls', namespace='billing', app_name='billing')),
    url(r'^extadmin/', include('main.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^moon/', include('moon.urls', namespace='moon', app_name='moon')),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
