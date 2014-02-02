from probill.billing.models import *

from django.core.management.base import BaseCommand

import random

class Command(BaseCommand):
    args = '<counter>'
    help = 'Handler for probill account copy'

    def handle(self, *args, **options):

        if len(args) > 1:
            if args[0] == 'change':
                if len(args) == 4:
                    tar = Tariff.objects.get(id=args[1])
                    network = args[2]
                    subscriber_names = args[3].split(',')
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
            elif args[0] == 'clean':
                subscriber_names = args[1].split(',')
                subscribers = Subscriber.objects.filter(login__in=subscriber_names)
                for sub in subscribers:
                    old_account = None
                    new_account = None
                    accounts = sub.account_set.all()
                    if len(accounts) == 2:
                        for account in accounts:
                            if account.login.startswith('auto__copy__'):
                                new_account = account
                            else:
                                old_account = account
                        if new_account and old_account:

                            old_account.ip = new_account.ip
                            old_account.mac = new_account.mac
                            new_account.ip = "0.0.0.0"
                            new_account.mac = None
                            PeriodicLog.log("Clean account {} MAC: {} IP: {}".format(new_account,
                                            old_account.ip,
                                            old_account.mac))
                            new_account.save()
                            new_account.delete()
                            old_account.save()
                        else:
                            print "Subscriber {} have >2 account".format(sub)
                    else:
                        print "Subscriber {} have >2 account".format(sub)
