from datetime import datetime, timedelta

from django.db.models import Sum
from django.core.management.base import BaseCommand, CommandError

from probill.billing.models import  TrafficByPeriod, Account, Subscriber


class Command(BaseCommand):
    args = '<counter>'
    help = 'Handler for billing status'

    def handle(self, *args, **options):
        if len(args) == 1:
            command = args[0]
            if command == 'active_session':
                query = TrafficByPeriod.objects.filter(datetime__gte=datetime.now()-timedelta(minutes=30))
                query = query.distinct('account').count()
                print query
            elif command == 'account_count':
                query = Account.objects.filter().count()
                print query
            elif command == 'active_account_count':
                query = Account.objects.filter(active=True).count()
                print query
            elif command == 'blocked_account_count':
                query = Account.objects.filter(active=False).count()
                print query
            elif command == 'subscriber_balance':
                query = Subscriber.objects.aggregate(balance_sum=Sum('balance'))
                print query['balance_sum']
            else:
                raise CommandError('Unknown command {}'.format(command))
        else:
            raise CommandError('Invalid args length')