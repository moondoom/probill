from billing.models import *

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = '<counter>'
    help = 'Handler for probill database merge'

    def handle(self, *args, **options):
        if len(args) > 0:
            source_db = args[0]
        else:
            raise Exception
        subscribers = Subscriber.objects.using(source_db)
        for subscriber in subscribers:
            account = subscriber.account_set.all()
            print account
            subscriber.pk = None
            subscriber.save()

