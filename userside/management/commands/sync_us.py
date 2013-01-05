from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from userside.models import TblBase, TblIp, TblGroup, TblStreet, TblHouse
from billing.models import Subscriber, Tariff


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
        'logpass',
        'fio',
        'podezd',
        'housec',
        'apart',
        'apart_b',
        'balans',
        'tel',
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


    def sync_users(self):
        billing_users = {}
        for user in Subscriber.objects.all():
            billing_users[user.login] = user
        for user in TblBase.objects.using('userside').all():
            if user.logname in billing_users:
                self.check_user(billing_users[user.logname],user)
                del billing_users[user.logname]
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

    def create_user(self,user):
        p2u_user = self.get_us_user(user)
        p2u_user.save(using='userside')

    def get_us_tariff(self,tariff):
        return TblGroup(
            code='probill_{}'.format(tariff.pk),
            groupname=tariff.name,
            abon=tariff.rental,
            speedtx=tariff.qos_speed,
            speedrx=tariff.qos_speed,
        )



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
        flat_int, flat_char = self.parse_int_char(user.address_flat)
        return TblBase(
            logname = user.login,
            logpass = user.password,
            fio = ' '.join([f for f in (user.first_name, user.last_name, user.father_name) if f]),
            housec = house,
            apart = flat_int or None,
            apart_b = flat_char or None,
            tel = user.phone,
            balans = user.balance,
        )

    def create_tariff(self,tariff):
        self.get_us_tariff(tariff).save(using='userside')
        return True

    def check_tariff(self,p_tariff,u_tariff):
        p2u_tariff = self.get_us_tariff(p_tariff)
        if not self.compare_object(u_tariff,p2u_tariff,self.tariff_params):
            u_tariff.save(using='userside')
        return True

    def check_user(self,p_user,u_user):
        p2u_user = self.get_us_user(p_user)
        if not self.compare_object(u_user,p2u_user,self.user_params):
            u_user.save(using='userside')
        else:
            return


    def handle(self, *args, **options):
        self.sync_tariff()
        self.sync_users()



