# -*- coding: utf-8 -*-

from django.contrib import admin

from lib.admin_models import FastDelete
#from django import forms
from models import *

admin.site.disable_action('delete_selected')


class MySubscriberAdmin(FastDelete):
    list_display = ['first_name', 'last_name', 'region', 'login', 'password', 'address_street',
                    'address_house', 'address_flat', 'balance', 'need_change_password', 'deleted']
    list_filter = ['region',]
    search_fields = ['first_name', 'last_name', 'address_street', 'address_house', 'address_flat', 'login']
    ordering = ['region','first_name']



class MyAccountAdmin(FastDelete):
    list_display = ['__unicode__', 'ip', 'mac','tariff', 'login',
                    'block_date', 'status', 'active',
                    'auto_block', 'deleted']
    search_fields = ('login', 'subscriber__first_name', 'subscriber__login', 'ip', 'mac',
                     'subscriber__last_name', 'tariff__name', 'block_date')
    list_filter = ('subscriber__region',)
    ordering = ['subscriber','login']


class MyTrafficByPeriodAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'account', 'tariff', 'qac_class', 'count', 'cost')
    search_fields = ('datetime',)
    ordering = ['-datetime', '-count']


class MyTrafficDetailAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'account', 'src_ip','dst_ip','count')
    search_fields = ('datetime',)


class MyLogAdmin(admin.ModelAdmin):
    list_display = ('datetime','message','code')
    search_fields = ('datetime','message')


class MyAccHistAdmin(admin.ModelAdmin):
    list_display = ('datetime','subscriber','value', 'owner_type')
    search_fields = ('datetime', 'subscriber__first_name', 'subscriber__first_name', 'subscriber__account__login',)
    ordering = ['-datetime']

class MyOSMPPayAdmin(admin.ModelAdmin):
    list_display = ('process_date', 'command', 'value', 'result', 'osmp_txn_id','comment')
    search_fields = ('osmp_txn_id', 'comment')
    list_filter = ('result', 'command',)


class MyTariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'rental', 'qos_speed', 'speed_up',
                    'speed_up_start', 'speed_up_end', 'get_account_count',
                    'use_traffic_threshold')

    def has_delete_permission(self, request, obj=None):
        return False

    def queryset(self,request):
        return super(MyTariffAdmin, self).queryset(request).exclude(archive=True)


class MyTrustPayAdmin(admin.ModelAdmin):
    list_display = ('create_date', 'end_date','subscriber','value', 'trust_days')
    search_fields = ('subscriber__first_name', 'subscriber__last_name',
                     'subscriber__login', 'subscriber__account__login')
    ordering = ['create_date']

class MyAccountLogAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'account','old_status','new_status')
    search_fields = ('account__login', 'account__subscriber__first_name','account__subscriber__last_name')
    ordering = ['datetime']


admin.site.register(Region)
admin.site.register(Subscriber,MySubscriberAdmin)
admin.site.register(Account,MyAccountAdmin)
admin.site.register(TrafficByPeriod,MyTrafficByPeriodAdmin)
admin.site.register(PeriodicLog,MyLogAdmin)
admin.site.register(AccountHistory,MyAccHistAdmin)
admin.site.register(TrustPay,MyTrustPayAdmin)
admin.site.register(AccountLog,MyAccountLogAdmin)
admin.site.register(OsmpPay, MyOSMPPayAdmin)
admin.site.register(Manager)
admin.site.register(Subnets)
admin.site.register(QosAndCost)
admin.site.register(Tariff, MyTariffAdmin)



