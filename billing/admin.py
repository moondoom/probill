# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *



admin.site.register(Manager)
admin.site.register(Subscriber)
admin.site.register(Account)
admin.site.register(Subnets)
admin.site.register(QosAndCost)
admin.site.register(Tariff)
admin.site.register(AccountHistory)
admin.site.register(TrafficByPeriod)
admin.site.register(PeriodicLog)

