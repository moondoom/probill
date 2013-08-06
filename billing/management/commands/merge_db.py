from billing.models import *

from django.core.management.base import BaseCommand
from django.contrib.admin.models import User
from django.core.exceptions import ObjectDoesNotExist
class Command(BaseCommand):
    args = '<counter>'
    help = 'Handler for probill database merge'

    def handle(self, *args, **options):
        subscribers = Subscriber.objects.using('merge_from')
        for subscriber in subscribers:
            accounts = subscriber.account_set.using('merge_from').all()
            account_history = subscriber.accounthistory_set.using('merge_from').all()
            subscriber.pk = None
            system_user_name = subscriber.owner.system_user.username
            try:
                system_user = Manager.objects.get(system_user__username=system_user_name)
            except ObjectDoesNotExist:
                system_user = Manager.objects.all()[0]
            subscriber.owner_id = system_user.id
            region_name = subscriber.region.name
            try:
                region = Region.objects.get(name=region_name)
            except ObjectDoesNotExist:
                region = Region.objects.all()[0]
            subscriber.region_id = region.id

            subscriber.save(using='default', process=False, force_insert=True)
            print subscriber.id
            for account in accounts:
                account.pk = None
                if account.tariff:
                    tariff_name = account.tariff.name
                    try:
                        tariff = Tariff.objects.get(name=tariff_name)
                    except ObjectDoesNotExist:
                        tariff = Tariff.objects.all()[0]
                    account.tariff_id = tariff.id
                account.owner_id = system_user.id
                account.subscriber_id = subscriber.id
                account.save(using='default', process=False, force_insert=True)
            for ah in account_history:
                print ah
                ah.pk = None
                ah.owner_id = 0
                if ah.owner_type == 'us':
                    ah.owner_type = 'syn'
                elif ah.owner_type == 'man':
                    try:
                        old_manager = Manager.objects.using('merge_from').get(id=ah.owner_id)
                        new_manager = Manager.objects.get(system__user_name=old_manager.system_user.username)
                        ah.owner_id = new_manager.id
                    except ObjectDoesNotExist:
                        ah.owner_id = Manager.objects.all()[0].id
                ah.subscriber_id = subscriber.id
                ah.save(using='default', process=False, force_insert=True)
