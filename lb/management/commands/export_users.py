__author__ = 'animage'

from django.core.management.base import BaseCommand
from settings import *
from lb.lib.mikrotik import Firewall
from suds.client import Client
from suds import WebFault
from billing.models import PeriodicLog, Subscriber, Account
from lb.models import *


class Command(BaseCommand):
    args = ''
    help = 'Firewall setup'

    def create_address(self, cl, exp_sub):
        pass

    def create_dog(self, cl, exp_sub):
        pass

    def create_vgroups(self, cl, exp_sub):
        pass

    def create_accounts(self, cl, sub):
#        sub = Subscriber.objects.get()
        new_acc = cl.factory.create('soapAccountFull')

        new_acc.account.login = sub.login
        new_acc.account['pass'] = sub.password
        new_acc.account.abonentname = sub.last_name
        new_acc.account.abonentsurname = sub.first_name,
        new_acc.account.abonentpatronymic = sub.father_name,
        new_acc.account.email = sub.email,
        new_acc.account.mobile = sub.phone.replace('+', ''),


        new_acc.account.uid = cl.service.insupdAccount(val=new_acc, isInsert=long(1))
        flt = cl.factory.create('flt')
        flt.login = sub.login
        exp_sub = ExportedSub(
            subscriber=sub,
            lb_id=new_acc.account.uid
        )
        exp_sub.save()
        self.create_dog(cl, exp_sub)
        self.create_vgroups(cl, exp_sub)
        self.create_address(cl, exp_sub)



    def handle(self, *args, **options):
        if LB_ENABLE:
            cl = Client(LB_SOAP_URL)
            cl.service.Login(LB_USERNAME, LB_PASSWORD)
        else:
            return
        if len(args) >= 2:
            if args[0] == 'login':
                sub = Subscriber.objects.get(login=args[1])
                self.create_accounts(cl, sub)






