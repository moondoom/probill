from django.conf.urls.defaults import patterns, url, include
from views import *
from moon_views import *


urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^info$', index,{'template': 'client_info.html'}),
    url(r'^money$', index,{'template': 'client_money.html'}),
    url(r'^stat$', index,{'template': 'client_stat.html'}),
    url(r'^stat/json/$', stat_json),
    url(r'^support$', index),
    url(r'^login$', login),
    url(r'^logout$', logout),
    #moon_views
    url(r'^subscriber/', include(subscriber_grid.urls)),
    url(r'^account/', include(account_grid.urls)),
    url(r'^accounthistory/', include(accounthistory_grid.urls)),
    url(r'^tariff/', include(tariff_grid.urls)),
    url(r'^tariffhistory/', include(tariffhistory_grid.urls)),
    url(r'^subnets/', include(subnets_grid.urls)),
    url(r'^qosandcost/', include(qosandcost_grid.urls)),
    url(r'^manager/', include(manager_grid.urls)),
    url(r'^periodiclog/', include(periodiclog_grid.urls)),
    url(r'^trafficbyperiod/', include(trafficbyperiod_grid.urls)),
    url(r'^trafficdetail/', include(trafficdetail_grid.urls)),
)
