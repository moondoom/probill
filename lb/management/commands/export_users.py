# coding=utf-8
__author__ = 'animage'

from django.core.management.base import BaseCommand
from settings import *
from lb.lib.mikrotik import Firewall
from suds.client import Client
from suds import WebFault
from billing.models import PeriodicLog, Subscriber, Account
from lb.models import *
from userside.models_v3 import TblBaseDopdata, TblBase
from datetime import date

class Command(BaseCommand):
    args = ''
    help = 'Firewall setup'
    us_ext_attr = dict(LB_US_DOPDATA)
    us_tar_list = {}

    def copy_obj(self,cl, src, dst_temp):
        dst = cl.factory.create(dst_temp)
        for k in src:
            dst[k[0]] = src[k[0]]
        return dst


    def create_vgroups(self, cl, exp_sub):
        flt = cl.factory.create('flt')
        flt.userid =  exp_sub.lb_id
        vgroups = cl.service.getVgroups(flt)
        for x in vgroups:
            cl.service.delVgroup(x.vgid)

        if not self.us_tar_list:
            for x in cl.service.getTarifs():
                self.us_tar_list[x.name.encode('utf-8')] = x.id
        accounts = exp_sub.subscriber.account_set.all()

        lb_acc = cl.service.getAccount(id=exp_sub.lb_id)[0]

        pay = cl.factory.create('soapPayment')
        pay.agrmid = lb_acc['agreements'][0].agrmid
        pay.receipt = "{}_init".format(exp_sub.subscriber.login)
        pay.amount = exp_sub.subscriber.balance
        cl.service.Payment(val=pay)

        for account in accounts:
            vg = cl.factory.create('soapVgroupFull')
            vg.vgroup.login = "{}-{}".format(exp_sub.subscriber.login, account.id)
            vg.vgroup['pass'] = exp_sub.subscriber.password
            vg.vgroup.amount = exp_sub.subscriber.balance
            vg.vgroup.id = int(LB_AGENT_ID)
            vg.vgroup.uid = exp_sub.lb_id
            vg.vgroup.agrmid = lb_acc['agreements'][0].agrmid

            #vg.vgroup.recordid = 0
            vg.vgroup.tarid = 0
            staff = cl.factory.create('soapStaff')
            staff.type = long(0)
            staff.ipmask.ip = str(account.ip)
            staff.ipmask.mask = long(32)
            vg.staff.append(staff)
            if account.interface:
                add = cl.factory.create('soapVgroupAddon')
                add.name = 'interface'
                add.strvalue = account.interface
                vg.addons.append(add)
            if account.mac:
                add = cl.factory.create('soapVgroupAddon')
                add.name = 'mac'
                add.strvalue = account.mac
                vg.addons.append(add)
            if account.tariff:
                if account.tariff.name.encode('utf-8') in self.us_tar_list:
                    tar = cl.factory.create('soapTarifsRasp')
                    tar.taridnew = self.us_tar_list[account.tariff.name.encode('utf-8')]
                    tar.taridold = long(0)
                    tar.agenttype = 4
                    tar.changetime = str(date.today())
                    vg.tarrasp.append(tar)
            else:
                print "Tariff {} not found".format(account.tariff)
            try:
                vg_id = cl.service.insupdVgroup(val=vg, isInsert=long(1))
            except WebFault as e:
                print exp_sub.subscriber, e

            #vg = cl.service.getVgroup(vg_id)[0]
            #print vg
            #vg = self.copy_obj(cl, vg, 'soapVgroupFull')

            #print vg
            #vg_id = cl.service.insupdVgroup( val=vg , isInsert=long(0))

    def get_address(self, cl, sub):
        flt = cl.factory.create('soapAddressFilter')
        flt.country = 1
        flt.region = 1
        flt.name = sub.region.name
        cities = cl.service.getAddressCities(flt)

        if cities:
            flt.city = cities[0].recordid
        else:
            city = cl.factory.create('soapAddressCity')
            city.name = unicode(sub.region.name)
            city.shortname = u"г"
            city.region = 1
            flt.city = cl.service.insupdAddressCity(val=city, isInsert=long(1))

        flt.name = unicode(sub.address_street)
        streets = cl.service.getAddressStreets(flt)

        if streets:
            flt.street = streets[0].recordid
        else:
            street = cl.factory.create('soapAddressStreet')
            street.name = unicode(sub.address_street)
            street.shortname = u"ул"
            street.city = flt.city
            street.idx = 0
            street.region = flt.region

            flt.street = cl.service.insupdAddressStreet(val=street, isInsert=long(1))

        flt.name = unicode(sub.address_house)
        buildings = cl.service.getAddressBuildings(flt)
        if buildings:
            flt.building = buildings[0].recordid
        else:
            building = cl.factory.create('soapAddressBuilding')
            building.name = unicode(sub.address_house)
            building.shortname = u"д"
            building.street = flt.street
            building.region = flt.region
            flt.building = cl.service.insupdAddressBuilding(val=building, isInsert=long(1))

        flt.name = unicode(sub.address_flat)
        flats = cl.service.getAddressFlats(flt)
        if flats:
            flat = flats[0].recordid
        else:
            flat = cl.factory.create('soapAddressFlat')
            flat.name = unicode(flt.name)
            flat.shortname = u"кв"
            flat.building = flt.building
            flat.region = flt.region
            flat = cl.service.insupdAddressFlat(val=flat, isInsert=long(1))

        address_code = [
            flt.country,
            flt.region,
            0,
            flt.city,
            0,
            flt.street,
            flt.building,
            flt.flat,
            0,
            0
        ]
        return address_code

    def create_accounts(self, cl, sub):
#        sub = Subscriber.objects.get()
        exp_sub = None
        try:
            exp_sub = ExportedSub.objects.get(subscriber=sub)
        except Exception as e:
            flt = cl.factory.create('flt')
            flt.login = sub.login
            if cl.service.getAccounts(flt=flt):
                print sub, 'уже существует'
                return

            new_acc = cl.factory.create('soapAccountFull')
            address = cl.factory.create('soapAddressBrief')
            try:
                address.code = ','.join(map(str,self.get_address(cl, sub)))
                address.type = 0
                new_acc.addresses.append(address)
            except WebFault as e:
                print "Address {} not fount".format(sub)

            agrm = cl.factory.create('soapAgreement')
            agrm.balance = long(sub.balance)
            agrm.balanceacc = long(sub.balance)
            agrm.number = sub.login
            agrm.date = sub.create_date.strftime('%Y-%m-%d')
            agrm.operid = 1
            agrm.balancestatus = 4
            agrm.curid = 1
            new_acc.agreements.append(agrm)
            new_acc.account.type = 2
            new_acc.account['pass'] = sub.password
            new_acc.account.abonentname = sub.last_name
            new_acc.account.abonentsurname = sub.first_name,
            new_acc.account.abonentpatronymic = sub.father_name,
            new_acc.account.email = sub.email,
            new_acc.account.mobile = sub.phone.replace('+', ''),
            # us_base = TblBase.objects.filter(logname=sub.login).using('userside')
            # if us_base:
            #     us_base = us_base[0]
            #     us_attrs = TblBaseDopdata.objects.filter(usercode=us_base.code).using('userside')
            #
            #     for us_attr in us_attrs:
            #         if us_attr.datacode in self.us_ext_attr:
            #             new_acc.account[self.us_ext_attr[us_attr.datacode]] = us_attr.valuestr
            try:
                new_acc.account.uid = cl.service.insupdAccount(val=new_acc, isInsert=long(1))

                exp_sub = ExportedSub(
                    subscriber=sub,
                    lb_id=new_acc.account.uid
                )
                exp_sub.save()
            except WebFault as e:
                print e
                pass
            if exp_sub:

                self.create_vgroups(cl, exp_sub)




    def handle(self, *args, **options):
        if LB_ENABLE:
            cl = Client(LB_SOAP_URL)
            cl.service.Login(LB_USERNAME, LB_PASSWORD)
        else:
            return
        if len(args) >= 1:
            if args[0] == 'login' and len(args) == 2:
                sub = Subscriber.objects.get(login=args[1])
                self.create_accounts(cl, sub)
            elif args[0] == 'all':
                sub = Subscriber.objects.all()
                for x in sub:
                    self.create_accounts(cl, x)





