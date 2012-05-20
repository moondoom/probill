# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

class MySubscriberAdmin(admin.ModelAdmin):
    list_display = ('login','first_name','last_name','address_street','address_house','address_flat','balance',)
    search_fields = ('first_name','last_name','address_street','address_house','address_flat','login')

admin.site.register(Subscriber,MySubscriberAdmin)
admin.site.register(Manager,admin.ModelAdmin)
admin.site.register(Account)
admin.site.register(Subnets)
admin.site.register(QosAndCost)
admin.site.register(Tariff)
admin.site.register(AccountHistory)
admin.site.register(TrafficByPeriod)
admin.site.register(PeriodicLog)

