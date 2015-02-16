# coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from nas.lib.rosapi import Core
from settings import *
from lb.lib.mikrotik import Firewall
from suds.client import Client
from suds import WebFault
from billing.models import PeriodicLog


class Command(BaseCommand):
    args = ''
    help = 'Firewall setup'

    def get_account(self, cl):

        flt = cl.factory.create('soapFilter')
        flt.type = 4
        ac_brief = cl.service.getVgroups(flt=flt)
        account_dicts = {}
        for ac_d in ac_brief:
            try:
                ac_f = cl.service.getVgroup(id=ac_d.vgid)[0]
                ip = ac_f.macstaff[0].segment
                mac = ac_f.macstaff[0].mac
                interface = [f.strvalue for f in ac_f.addons if f.name == 'interface'][0]

                if ip in account_dicts:
                    PeriodicLog('Possible IP double (LOGIN: {} IP: {})'.format(ac_f.vgroup.login, ip))
                    continue
                if ac_f.vgroup.currentshape == 0:
                    blocked = True
                else:
                    blocked = ac_f.vgroup.blocked
                account_dicts[ip] = [
                    mac,
                    interface,
                    ac_f.vgroup.currentshape,
                    blocked,
                    ac_d.vgid
                ]
                #print account_dicts[ip]
            except WebFault as e:
                PeriodicLog(str(e))
                #print e
                continue
            except IndexError as e:
                PeriodicLog(str(e))
                #print e
                continue
            except AttributeError as e:
                PeriodicLog(str(e))
                continue
        if len(account_dicts) < 10:
            print self, "Account count < 10"
            raise CommandError
        return account_dicts

    def handle(self, *args, **options):
        if LB_ENABLE:
            cl = Client(LB_SOAP_URL)
            cl.service.Login(LB_USERNAME, LB_PASSWORD)
            fw = Firewall(LB_NAS_ID, self.get_account(cl))
            fw.sync_all()
            cl.service.Logout()




