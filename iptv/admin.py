# -*- coding: utf-8 -*-

from django.contrib import admin

from lib.admin_models import FastDelete
#from django import forms
from models import *


admin.site.register(AstraServer)
admin.site.register(AstraConfig)
admin.site.register(AstraChannel)
admin.site.register(LocalChannel)
admin.site.register(M3UPlayList)
admin.site.register(SSIPTVChannel)
admin.site.register(SSIPTVPlayList)
admin.site.register(SSIPTV2Channel)

