from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'moon.views.index', name='index'),
    url(r'^login$', 'django.contrib.auth.views.login', name='login',),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/moon/login'}, name='logout'),

)



