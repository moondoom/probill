# coding=utf-8
__author__ = 'animage'

from django.core.management.base import BaseCommand, CommandError
from settings import *
from suds.client import Client
from suds import WebFault

class Command(BaseCommand):
    args = '[login] [regions]'
#help = 'export users '


    def handle(self, *args, **options):
        if LB_ENABLE:
            cl = Client(LB_SOAP_URL)
            cl.service.Login(LB_USERNAME, LB_PASSWORD)
        else:
            return
        flt = cl.factory.create('soapFilter')
        flt.type = 4
        ac_brief = cl.service.getVgroups(flt=flt)
        for ac_d in ac_brief:
            try:
                ac_f = cl.service.getVgroup(id=ac_d.vgid)[0]
                #ac_f = cl.service.getVgroup(id=582)[0]
                if hasattr(ac_f, 'macstaff'):
                    print "{} have mac".format(ac_f.vgroup.login)
                    continue
                ip = ac_f.staff[0].ipmask.ip
                mac = [f.strvalue for f in ac_f.addons if f.name == 'mac'][0]
                if mac and ip:

                    lb_mac = cl.factory.create('soapMacStaff')
                    lb_mac.recordid = ac_f.staff[0].recordid
                    lb_mac.vgid = ac_f.vgroup.vgid
                    lb_mac.mac = mac
                    lb_mac.segment = ip
                    cl.service.insupdMacStaff(val=lb_mac, isInsert=long(1))
                    print "Create mac {} for {}".format(ac_f.vgroup.login, lb_mac.mac)
            except WebFault as e:
                print ac_d.login, e
                continue
            except IndexError as e:
                print ac_d.login, e
                continue
            except AttributeError as e:
                print ac_d.login, e
                continue






