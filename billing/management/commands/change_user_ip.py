from probill.billing.models import *

from django.core.management.base import BaseCommand
from ipaddr import IPNetwork

from nas.models import IPInterface, NetworkInterface

import random

class Command(BaseCommand):
    args = '<counter>'
    help = 'Handler for probill account copy'

    def handle(self, *args, **options):

        if len(args) > 1:
            if args[0] == 'change':
                if len(args) > 4:
                    tar = Tariff.objects.get(id=args[1])
                    net = IPNetwork(args[2])
                    query = Account.objects.filter(ip__in=net)
                    used_ip = [f.ip for f in query] + [net.broadcast, net.network]
                    free_ip = [f for f in net if f not in used_ip]
                    free_ip.reverse()
                    subscribers = Subscriber.objects.exclude(account__login__startswith='auto__copy')
                    n = 3
                    while len(args) > n:
                        if args[n] == "region":
                             subscribers = subscribers.filter(region__in=args[n + 1].split(','))
                        elif args[n] == "name":
                            subscribers = subscribers.filter(login__in=args[n + 1].split(','))
                        elif args[n] == "-name":
                            subscribers = subscribers.exclude(login__in=args[n + 1].split(','))
                        elif args[n] == "iface":
                            subscribers = subscribers.filter(account__interface=args[n + 1])
                        n += 2

                    for sub in subscribers:
                        for account in sub.account_set.all():
                            if account.mac:
                                new_account = Account(subscriber=sub,
                                                      login='auto__copy__{}'.format(account.login),
                                                      tariff=tar,
                                                      owner=account.owner,
                                                      ip=free_ip.pop(),
                                                      mac=account.mac,
                                                      active=account.active,
                                                      status=200,
                                                      interface=None)
                                account.mac = None
                                account.save()
                                new_account.save()
                                PeriodicLog.log("Copy account {} to {} MAC: {}".format(account,
                                                                                       new_account,
                                                                                       new_account.mac))
            elif args[0] == 'clean':
                filter_net = IPNetwork(args[1])
                subscribers = Subscriber.objects.filter(account__ip__in=filter_net).exclude(account__deleted=True)
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
                            old_account.interface = new_account.interface
                            new_account.ip = "0.0.0.0"
                            new_account.mac = None
                            PeriodicLog.log("Clean account {} MAC: {} IP: {}".format(new_account,
                                            old_account.ip,
                                            old_account.mac))
                            new_account.save()
                            new_account.delete()
                            old_account.save()
                        else:
                            print "Subscriber {} have <2 account".format(sub)
                    else:
                        print "Subscriber {} have >2 account".format(sub)

            elif args[0] == '2unnumbered':
                self.interface = {}
                for interface in NetworkInterface.objects.all():
                    self.interface[interface.name] = []
                    for net in IPInterface.objects.filter(iface=interface):
                        self.interface[interface.name].append(net.network)
                tar = Tariff.objects.get(id=args[1])
                filter_net = IPNetwork(args[2])
                free_ip = []
                for net in args[3:]:
                    white_net = IPNetwork(net)
                    query = Account.objects.filter(ip__in=white_net)
                    used_ip = [f.ip for f in query] + [white_net.broadcast, white_net.network]
                    free_ip += [f for f in white_net if f not in used_ip]
                free_ip.reverse()
                query = Subscriber.objects.filter(account__ip__in=filter_net)
                for sub in query:
                    if len(sub.account_set.all()) > 1:
                        continue
                    for account in sub.account_set.all():
                        print account.ip
                        interface = None
                        for name in self.interface:
                            for net in self.interface[name]:
                                if account.ip in net:
                                    interface = name
                                    break
                        if interface:
                            try:
                                new_account = Account(subscriber=sub,
                                                      login='auto__copy__{}'.format(account.login),
                                                      tariff=tar,
                                                      owner=account.owner,
                                                      ip=free_ip.pop(),
                                                      mac=account.mac,
                                                      status=200,
                                                      active=account.active,
                                                      interface=interface)
                            except IndexError as e:
                                print "No more free IP"
                                break
                            account.mac = None
                            account.save()
                            new_account.save()
                            PeriodicLog.log("Change account {} MAC: {} IP: {} to {} unnumbered".format(account,
                                                                                                new_account.mac,
                                                                                                account.ip,
                                                                                                new_account.ip))


