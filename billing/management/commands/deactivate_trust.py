from probill.billing.models import *

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = 'Deactivate trust pay'

    def handle(self, *args, **options):
        tps = TrustPay.objects.filter(active=True,end_date__lte=datetime.now())
        for tp in tps:
            tp.deactivate()


