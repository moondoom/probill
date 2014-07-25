# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *


class UpLinkPoliceAdmin(admin.ModelAdmin):
    filter_horizontal = ['accounts']



class NetFlowAdmin(admin.ModelAdmin):
    list_display = ('nas', 'file_time', 'file_dir', 'file_name')


class MyNasServer(admin.ModelAdmin):
    list_display = ('name', 'mng_ip', 'active', 'local')

class MyNetworkInterface(admin.ModelAdmin):
    list_display = ('nas', 'name')

class MyIPInterface(admin.ModelAdmin):
    list_display = ('iface',  'network')


class MyUpLink(admin.ModelAdmin):
    list_display = ('nas',  'local_address', 'remote_address', 'priority', 'enabled', 'active')


class BlackListAdmin(admin.ModelAdmin):
    list_display = ('add_datetime', 'ip',)
    search_fields = ('ip', 'description')

admin.site.register(NasServer, MyNasServer)
admin.site.register(IPInterface, MyIPInterface)
admin.site.register(NetworkInterface, MyNetworkInterface)
admin.site.register(DHCPServer)

admin.site.register(DHCPSubnet)
admin.site.register(UpLink, MyUpLink)
admin.site.register(UpLinkPolice, UpLinkPoliceAdmin)
admin.site.register(NetFlowProcessor)
admin.site.register(NetFlowSource, NetFlowAdmin)
admin.site.register(Firewall)
admin.site.register(BlackListByIP, BlackListAdmin)

