from django.conf.urls.defaults import patterns, url, include
from views import *
from moon_views import *


urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^info$', index, {'template': 'client_info.html'}),
    url(r'^money$', index, {'template': 'client_money.html'}),
    url(r'^stat$', index, {'template': 'client_stat.html'}),
    url(r'^trust$', trust_pay),
    url(r'^pay$', pay),
    url(r'^visa$', visa_gpb, name='visa'),
    url(r'^visa/fail$', visa_gpb, {'command': 'fail'}, name='visa_fail'),
    url(r'^visa/success$', visa_gpb, {'command': 'success'}, name='visa_success'),
    url(r'^visa/check$', visa_gpb_no_auth, {'command': 'check'}, name='visa_check'),
    url(r'^visa/pay$', visa_gpb_no_auth, {'command': 'pay'}, name='visa_pay'),
    url(r'^change_password', change_password),
    url(r'^stat/json/$', stat_json),
    url(r'^support$', index),
    url(r'^login$', login),
    url(r'^blocked$', only_ip_auth),
    url(r'^osmp$', osmp_gate),
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
