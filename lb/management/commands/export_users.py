# coding=utf-8
__author__ = 'animage'

from django.core.management.base import BaseCommand
from settings import *
from suds.client import Client
from suds import WebFault
from billing.models import Subscriber
from lb.models import *
import random
from datetime import date
from nas.models import NetworkInterface, IPInterface

class Command(BaseCommand):
    args = '[login] [regions]'
#help = 'export users '
    us_ext_attr = dict(LB_US_DOPDATA)
    us_tar_list = {}
    region_map = {}
    interface = {}

    def copy_obj(self,cl, src, dst_temp):
        dst = cl.factory.create(dst_temp)
        for k in src:
            dst[k[0]] = src[k[0]]
        return dst

    def find_interface(self, account):
        if account.interface:
            return account.interface
        for interface in self.interface:
            for net in self.interface[interface]:
                if account.ip in net:
                    return interface
        return 'all'

    def create_vgroups(self, cl, exp_sub):
        flt = cl.factory.create('flt')
        flt.userid = exp_sub.lb_id
        vgroups = cl.service.getVgroups(flt)
        for x in vgroups:
            cl.service.delVgroup(x.vgid)

        if not self.us_tar_list:
            for x in cl.service.getTarifs():
                self.us_tar_list[x.name.encode('utf-8')] = x.id
        accounts = exp_sub.subscriber.account_set.all()

        lb_acc = cl.service.getAccount(id=exp_sub.lb_id)[0]

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
            add = cl.factory.create('soapVgroupAddon')
            add.name = 'interface'
            add.strvalue = self.find_interface(account)
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
                    #tar.taridold = long(0)
                    tar.agenttype = 4
                    tar.changetime = str(date.today())
                    vg.tarrasp.append(tar)
                else:
                    print "Tariff {} not found".format(account.tariff)
            vg.vgroup.blocked = 0
            block = cl.factory.create('soapBlockRasp')
            if account.active:
                block.blkreq = 0
            else:
                if exp_sub.subscriber.balance >= 0:
                    block.blkreq = 3
                else:
                    block.blkreq = 1

            block.requestby = 7
            block.changetime = str(date.today())
            vg.blockrasp.append(block)

            try:
                vg_id = cl.service.insupdVgroup(val=vg, isInsert=long(1))
            except WebFault as e:
                print exp_sub.subscriber, e

        lb_acc = cl.service.getAccount(id=exp_sub.lb_id)[0]


        pay = cl.factory.create('soapPayment')
        pay.agrmid = lb_acc['agreements'][0].agrmid
        pay.receipt = "{}_init_{}".format(exp_sub.subscriber.login, random.randint(1000, 1999))
        pay.amount = exp_sub.subscriber.balance - lb_acc.agreements[0].balance
        cl.service.Payment(val=pay)

            #vg = cl.service.getVgroup(vg_id)[0]
            #print vg
            #vg = self.copy_obj(cl, vg, 'soapVgroupFull')

            #print vg
            #vg_id = cl.service.insupdVgroup( val=vg , isInsert=long(0))



    def get_address(self, cl, sub):
        flt = cl.factory.create('soapAddressFilter')
        flt.country = 1
        flt.region = 1
        region_id = sub.region.id
        if self.region_map[region_id][0]:
            flt.city = self.region_map[region_id][0]
            flt.area = 0
            flt.settl = 0

        else:
            flt.area = self.region_map[region_id][1]
            flt.settl = self.region_map[region_id][2]
            flt.city = 0


        flt.name = unicode(sub.address_street)
        streets = cl.service.getAddressStreets(flt)

        if streets:
            flt.street = streets[0].recordid
        else:
            street = cl.factory.create('soapAddressStreet')
            street.name = unicode(sub.address_street)
            street.shortname = u"ул"
            street.city = flt.city
            street.region = 1
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
            building.city = flt.city
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
            flt.area,
            flt.city,
            flt.settl,
            flt.street,
            flt.building,
            flat,
            0,
            0
        ]
        return address_code

    def create_accounts(self, cl, sub):
#        sub = Subscriber.objects.get()
        exp_sub = None
        # try:
        #     exp_sub = ExportedSub.objects.get(subscriber=sub)
        #except Exception as e:
        #     flt = cl.factory.create('flt')
        #     flt.login = sub.login
        #     if cl.service.getAccounts(flt=flt):
        #         print sub, 'уже существует'
        #         return

        new_acc = cl.factory.create('soapAccountFull')
        address = cl.factory.create('soapAddressBrief')
        try:
            address.code = ','.join(map(str, self.get_address(cl, sub)))
            address.type = 0
            new_acc.addresses.append(address)
        except WebFault as e:
            print e
            print "Address {} not fount".format(sub)

        agrm = cl.factory.create('soapAgreement')
        agrm.balance = long(sub.balance)
        agrm.balanceacc = long(sub.balance)
        agrm.number = sub.login
        agrm.date = sub.create_date.strftime('%Y-%m-%d')
        agrm.operid = 1
        agrm.balancestatus = 1
        agrm.curid = 1
        agrm.paymentmethod = 2
        new_acc.agreements.append(agrm)
        new_acc.account.type = 2
        new_acc.account['pass'] = sub.password
        new_acc.account.login = sub.login
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
            #exp_sub.save()
        except WebFault as e:
            print sub, e
            pass
        if exp_sub:

            self.create_vgroups(cl, exp_sub)

    def parse_regions(self,reg_list):
        for reg in reg_list:
            reg = map(int, reg.split(':'))
            self.region_map[reg[0]] = reg[1:]

    def handle(self, *args, **options):
        for interface in NetworkInterface.objects.filter(nas__id=LB_NAS_ID):
            self.interface[interface.name] = []
            for net in IPInterface.objects.filter(iface=interface):
                self.interface[interface.name].append(net.network)
        if LB_ENABLE:
            cl = Client(LB_SOAP_URL)
            cl.service.Login(LB_USERNAME, LB_PASSWORD)
        else:
            return
        if len(args) >= 2:
            if args[0] == 'login' and len(args) == 2:
                sub = Subscriber.objects.get(login=args[1])
                self.create_accounts(cl, sub)
            elif args[0] == 'all':
                sub = Subscriber.objects.all()
                if args[1] != 'all':
                    self.parse_regions(args[1].split(','))

                    sub = sub.filter(region__id__in=self.region_map.keys())
                for x in sub:
                    self.create_accounts(cl, x)





