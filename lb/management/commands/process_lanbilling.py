# coding=utf-8

from django.core.management.base import BaseCommand
from nas.lib.rosapi import Core
from settings import *
from lb.lib.mikrotik import Firewall
from suds.client import Client
from suds import WebFault
from billing.models import PeriodicLog

class Command(BaseCommand):
    args = ''
    help = 'Firewall setup'

    def handle(self, *args, **options):
        if LB_ENABLE:
            cl = Client(LB_SOAP_URL)
            cl.service.Login(LB_USERNAME, LB_PASSWORD)
            print LB_USERNAME, LB_PASSWORD, LB_SOAP_URL
            flt = cl.factory.create('flt')
            flt.type = 4
            ac_brief = cl.service.getVgroups(flt=flt)
            account_dicts = {}
            for ac_d in ac_brief:
                try:
                    ac_f = cl.service.getVgroup(id=ac_d.id)[0]
                    ip = ac_f.macstaff[0].segment
                    interface = [f.strvalue for f in ac_f.addons if f.name == 'interface'][0]
                    if ip in account_dicts:
                        PeriodicLog('Possible IP double (LOGIN: {} IP: {})'.format(ac_f.login, ip))
                        continue
                    account_dicts[ip] = [
                        ac_f.mac_staff[0].mac,
                        interface,
                        ac_f.blocked,
                        ac_f.currentshape
                    ]
                    print account_dicts[ip]
                except WebFault as e:
                    #PeriodicLog(str(e))
                    print e
                    continue
                except IndexError as e:
                    #PeriodicLog(str(e))
                    print e
                    continue




