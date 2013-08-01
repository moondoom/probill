# -*- coding: utf-8 -*-

from django.contrib import admin

from lib.admin_models import FastDelete
#from django import forms
from models import *

admin.site.disable_action('delete_selected')




class MySubscriberAdmin(FastDelete):
    list_display = ('first_name','last_name','region','login','address_street','address_house','address_flat','balance')
    search_fields = ('first_name','last_name','address_street','address_house','address_flat','login')
    ordering = ['region','first_name']


class MyAccountAdmin(FastDelete):
    list_display = ('subscriber', 'login','ip', 'tariff', 'block_date', 'active', 'auto_block')
    search_fields = ('login','ip', 'tariff', 'block_date')
    ordering = ['subscriber','login']



class MyTrafficByPeriodAdmin(admin.ModelAdmin):
    list_display = ('datetime','account','qac_class','count','cost')
    search_fields = ('datetime',)


class MyTrafficDetailAdmin(admin.ModelAdmin):
    list_display = ('datetime','account','src_ip','dst_ip','count')
    search_fields = ('datetime',)


class MyLogAdmin(admin.ModelAdmin):
    list_display = ('datetime','message','code')
    search_fields = ('datetime','message')


class MyLogAdmin(admin.ModelAdmin):
    list_display = ('datetime','message','code')
    search_fields = ('datetime','message')


class MyAccHistAdmin(admin.ModelAdmin):
    list_display = ('datetime','subscriber','value')
    search_fields = ('datetime',)


admin.site.register(Region)
admin.site.register(Subscriber,MySubscriberAdmin)
admin.site.register(Account,MyAccountAdmin)
admin.site.register(TrafficByPeriod,MyTrafficByPeriodAdmin)
admin.site.register(TrafficDetail,MyTrafficDetailAdmin)
admin.site.register(PeriodicLog,MyLogAdmin)
admin.site.register(AccountHistory,MyAccHistAdmin)
admin.site.register(Manager)
admin.site.register(Subnets)
admin.site.register(QosAndCost)
admin.site.register(Tariff)





