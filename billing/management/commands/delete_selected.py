from billing.models import *

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = 'Delete selected object'

    def handle(self, *args, **options):
        subscribers = Subscriber.objects.filter(deleted=True)
        for subscriber in subscribers:
            subscriber.delete(force_delete=True)
        accounts = Account.objects.filter(deleted=True)
        for account in accounts:
            account.delete(force_delete=True)

