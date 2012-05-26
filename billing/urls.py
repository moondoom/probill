from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^info$', index,{'template':'client/info.html'}),
    url(r'^money$', index,{'template':'client/money.html'}),
    url(r'^stat$', index,{'template':'client/stat.html'}),
    url(r'^support$', index),
    url(r'^login$', login),
    url(r'^logout$', logout),
)
