from probill.billing.models import *

from django.core.management.base import BaseCommand

import random

class Command(BaseCommand):
    args = '<counter>'
    help = 'Handler for probill account copy'

    def handle(self, *args, **options):

        if len(args) == 3:
            tar = Tariff.objects.get(id=args[0])
            network = args[1]
            subscriber_names = args[2].split(',')
            print subscriber_names
            subscribers = Subscriber.objects.filter(login__in=subscriber_names).\
                exclude(account__login__startswith='auto__copy')
            ip_range = [network + '.' + str(f) for f in range(10, 200)]
            ip_range.reverse()
            for sub in subscribers:
                for account in sub.account_set.all():
                    print account
                    if account.mac:
                        new_account = Account(subscriber=sub,
                                              login='auto__copy__{}'.format(account.login),
                                              tariff=tar,
                                              owner=account.owner,
                                              ip=ip_range.pop(),
                                              mac=account.mac,
                                              status=200)
                        account.mac = None
                        account.save()
                        new_account.save()
                        PeriodicLog.log("Copy account {} to {} MAC: {}".format(account,
                                                                               new_account,
                                                                               new_account.mac))