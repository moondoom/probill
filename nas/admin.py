# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *



admin.site.register(NasServer)
admin.site.register(IPInterface)
admin.site.register(NetworkInterface)
admin.site.register(DHCPServer)
admin.site.register(DHCPSubnet)
admin.site.register(UpLink)
admin.site.register(UpLinkPolice)

