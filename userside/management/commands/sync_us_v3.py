from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from userside.models_v3 import TblBase, TblIp, TblGroup, TblStreet, TblHouse, TblBilhist, TblUnkmac

from billing.models import Subscriber, Tariff, Account, AccountHistory


import re

class Command(BaseCommand):
    args = ''
    help = 'Handler for sync Probill and Userside'
    int_char_split=re.compile(r'(\d+)[ /]*(.*)')
    tariff_params = (
        'abon',
        'speedtx',
        'speedrx',
        )
    user_params = (
        'logname',
        'pass_field',
        'fio',
        'podezd',
        'housec',
        'apart',
        'apart_b',
        'balans',
        'telmob',
        'tel',
        'groupn',
        )
    ip_params = (
        'usercode',
        'mac',
        'typer',
        )

    def compare_object(self,obj_a,obj_b,attr_list):
        result = True
        for attr in attr_list:
            if getattr(obj_a,attr) <> getattr(obj_b,attr):
                setattr(obj_a,attr,getattr(obj_b,attr))
                result = False
        return result

    def parse_int_char(self,string):
        str_math = re.match(self.int_char_split,string)
        if str_math:
            str_int , str_char = str_math.groups()
        else:
            str_int , str_char = None , None
        return str_int, str_char

    def sync_ip(self,p_user,u_user):
        billing_ip = {}
        for ip in Account.objects.filter(subscriber=p_user):
            billing_ip[int(ip.ip)] = ip
        for ip in TblIp.objects.using('userside').filter(usercode=u_user.code,typer=1):
            if int(ip.userip) in billing_ip:
                self.check_ip(billing_ip[ip.userip],ip,u_user.code)
                del billing_ip[int(ip.userip)]
            else:
                ip.delete(using='userside')

        for ip in billing_ip:
            self.get_us_ip(billing_ip[ip],u_user.code).save(using='userside')

    def sync_users(self):
        billing_users = {}
        for user in Subscriber.objects.all():
            billing_users[user.login] = user
        for user in TblBase.objects.using('userside').all():
            if user.logname in billing_users:
                self.check_user(billing_users[user.logname],user)
                del billing_users[user.logname]
            else:
                pass
                #self.sync_ip(None,user)
                #user.delete(using='userside')
        for user in billing_users:
            self.create_user(billing_users[user])

    def sync_tariff(self):
        billing_tariff = {}
        for tar in Tariff.objects.all():
            billing_tariff[tar.name] = tar
        for tar in TblGroup.objects.using('userside').all():
            if tar.groupname in billing_tariff:
                self.check_tariff(billing_tariff[tar.groupname],tar)
                del billing_tariff[tar.groupname]
        for tar in billing_tariff:
            self.create_tariff(billing_tariff[tar])

    def sync_balance(self):
        us_order = {}
        for order in TblBilhist.objects.using('userside').exclude(pko=None):
            us_order[order.pko] = order
        query = AccountHistory.objects.filter(owner_type='us')
        for order in query.filter(owner_id__in=us_order.keys()):
            del us_order[order.owner_id]
        for order_id in us_order:
            order = us_order[order_id]
            try:
                u_user = TblBase.objects.using('userside').get(code=order.usercode)
                p_user = Subscriber.objects.get(login=u_user.logname)
            except ObjectDoesNotExist as error:
                continue
            AccountHistory(
                datetime=order.datedo,
                subscriber=p_user,
                value=order.summa,
                owner_type='us',
                owner_id=order.pko,
            ).save()
            print order.summa


    def get_us_user(self,user):
        try:
            street = TblStreet.objects.using('userside').get(street=user.address_street)
            house_int, house_char = self.parse_int_char(user.address_house)
            if house_int:
                house = TblHouse.objects.using('userside').get(
                    streetcode = street.code,
                    house = house_int,
                    house_b = house_char)
                house = house.code
            else:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist as error:
            house = None
            print error
        try:
            p_tariff = user.account_set.all()[0].tariff
            tariff = TblGroup.objects.using('userside').get(groupname=p_tariff.name)
            tariff = tariff.code
        except ObjectDoesNotExist as error:
            tariff = None
            print error
        except IndexError as error:
            tariff = None
            print error
        except AttributeError as error:
            tariff = None
            print error
        flat_int, flat_char = self.parse_int_char(user.address_flat)
        if user.phone.count(' ')>0:
            tel = []
            telmob = []
            phone_list = re.split(r' *',user.phone)
            for phone in phone_list:
                if len(phone) > 10:
                    telmob.append(phone)
                else:
                    tel.append(phone)
            tel = ','.join(tel) or ' '
            telmob = ','.join(telmob) or ' '
        else:
            tel = ' '
            telmob = user.phone
        return TblBase(
            logname = user.login,
            pass_field = user.password,
            fio = ' '.join([f for f in (user.first_name, user.last_name, user.father_name) if f]),
            housec = house,
            apart = flat_int or None,
            apart_b = flat_char or '',
            tel = tel,
            telmob = telmob,
            balans = user.balance,
            groupn = tariff,
            #billcode = user.id
        )

    def create_user(self,user):
        p2u_user = self.get_us_user(user)
        p2u_user.save(using='userside')
        try:
            u_user = TblBase.objects.using('userside').get(logname=user.login)
            self.sync_ip(user,p2u_user)
        except ObjectDoesNotExist as error:
            print "Egor!"

    def check_user(self,p_user,u_user):
        p2u_user = self.get_us_user(p_user)
        if not self.compare_object(u_user,p2u_user,self.user_params):
            u_user.save(using='userside')
        self.sync_ip(p_user,u_user)

    def get_us_tariff(self,tariff):
        return TblGroup(
            code='probill_{}'.format(tariff.pk),
            groupname=tariff.name,
            abon=tariff.rental,
            speedtx=tariff.qos_speed,
            speedrx=tariff.qos_speed,
        )

    def create_tariff(self,tariff):
        self.get_us_tariff(tariff).save(using='userside')
        return True

    def check_tariff(self,p_tariff,u_tariff):
        p2u_tariff = self.get_us_tariff(p_tariff)
        if not self.compare_object(u_tariff,p2u_tariff,self.tariff_params):
            u_tariff.save(using='userside')


    def get_us_ip(self,ip,u_code):
        return TblIp(
            typer = 1,
            usercode = u_code,
            userip = int(ip.ip),
            mac = ''.join(ip.mac.split(':'))
        )


    def check_ip(self,p_ip,u_ip,u_code):
        p2u_tariff = self.get_us_ip(p_ip,u_code)
        if not self.compare_object(u_ip,p2u_tariff,self.ip_params):
            u_ip.save(using='userside')
        if u_ip.mac:
            for x in TblUnkmac.objects.using("userside").filter(mac = u_ip.mac):
                print "Delete", x.code, x.mac
                x.delete(using="userside")



    def ah_to_us(self):
        AccountHistory.objects.filter(type='syn')


    def handle(self, *args, **options):
        if len(args) > 0:
            if 'ah_to_us' in args:
                self.ah_to_us()
        self.sync_balance()
        self.sync_tariff()
        self.sync_users()
