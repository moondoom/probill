from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^info$', index),
    url(r'^money$', index),
    url(r'^stat$', index),
    url(r'^support$', index),
)
