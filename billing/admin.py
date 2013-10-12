# -*- coding: utf-8 -*-

from django.contrib import admin

from lib.admin_models import FastDelete
#from django import forms
from models import *

admin.site.disable_action('delete_selected')




class MySubscriberAdmin(FastDelete):
    list_display = ['first_name','last_name','region','login','address_street','address_house','address_flat','balance', 'deleted']
    list_filter = ['region',]
    search_fields = ['first_name', 'last_name', 'address_street', 'address_house','address_flat','login']
    ordering = ['region','first_name']


class MyAccountAdmin(FastDelete):
    list_display = ['subscriber', 'login','ip', 'mac','tariff',
                    'block_date', 'active',
                    'auto_block', 'deleted']
    search_fields = ('login', 'subscriber__first_name', 'ip', 'mac', 'subscriber__last_name', 'tariff__name', 'block_date')
    list_filter = ('subscriber__region',)
    ordering = ['subscriber','login']


class MyTrafficByPeriodAdmin(admin.ModelAdmin):
    list_display = ('datetime','account','qac_class','count','cost',)
    search_fields = ('datetime',)
    ordering = ['-datetime', '-count']


class MyTrafficDetailAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'account', 'src_ip','dst_ip','count')
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


class MyOSMPPayAdmin(admin.ModelAdmin):
    list_display = ('process_date', 'pay_date', 'command', 'value', 'result', 'osmp_txn_id', 'prv_txn')
    search_fields = ('osmp_txn_id', 'comment')
    list_filter = ('result', 'command')


class MyTariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'rental', 'qos_speed', 'speed_up', 'speed_up_start', 'speed_up_end', 'get_account_count')

    def has_delete_permission(self, request, obj=None):
        return False

    def queryset(self,request):
        return super(MyTariffAdmin, self).queryset(request).exclude(archive=True)

admin.site.register(Region)
admin.site.register(Subscriber,MySubscriberAdmin)
admin.site.register(Account,MyAccountAdmin)
admin.site.register(TrafficByPeriod,MyTrafficByPeriodAdmin)
admin.site.register(PeriodicLog,MyLogAdmin)
admin.site.register(AccountHistory,MyAccHistAdmin)
admin.site.register(OsmpPay, MyOSMPPayAdmin)
admin.site.register(Manager)
admin.site.register(Subnets)
admin.site.register(QosAndCost)
admin.site.register(Tariff, MyTariffAdmin)





