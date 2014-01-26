from probill.billing.models import *

from django.core.management.base import BaseCommand

import random

class Command(BaseCommand):
    args = '<counter>'
    help = 'Handler for probill database merge'

    def handle(self, *args, **options):

        if len(args) == 4:
            sub = Subscriber.objects.get(id=args[0])
            tar = Tariff.objects.get(id=args[1])
            man = Manager.objects.get(id=args[2])
            Account.objects.filter(login__startswith='demo_load_').delete()
            for y in range(1,2):
                for x in range(10,80):
                    Account(subscriber=sub,
                            tariff=tar,
                            owner=man,
                            ip=args[3] + str(y) + '.' + str(x),
                            mac='00:11:22:33:' + hex(y)[2:].zfill(2) + ':' +  hex(x)[2:].zfill(2),
                            login='demo_load_' + str(y) + '_' + str(x)).save()
        elif len(args) == 1:
            if args[0] == 'remove':
                Account.objects.filter(login__startswith='demo_load_').delete()
            elif args[0] == 'random':
                tars = [f for f in Tariff.objects.all()]
                tars.append(None)
                print tars

                for acc in Account.objects.filter(login__startswith='demo_load_'):

                    acc.tariff = random.choice(tars)
                    print acc, acc.active, acc.tariff
                    acc.save()
                    acc.status = 200
                    acc.active = random.choice([True, False])
                    acc.save()