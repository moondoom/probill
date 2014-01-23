# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *


class UpLinkPoliceAdmin(admin.ModelAdmin):
    filter_horizontal = ['accounts']



class NetFlowAdmin(admin.ModelAdmin):
    list_display = ('nas', 'file_time', 'file_dir', 'file_name')


admin.site.register(NasServer)
admin.site.register(IPInterface)
admin.site.register(NetworkInterface)
admin.site.register(DHCPServer)

admin.site.register(DHCPSubnet)
admin.site.register(UpLink)
admin.site.register(UpLinkPolice,UpLinkPoliceAdmin)
admin.site.register(NetFlowProcessor)
admin.site.register(NetFlowSource, NetFlowAdmin)
admin.site.register(Firewall)

