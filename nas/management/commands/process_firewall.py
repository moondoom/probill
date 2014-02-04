from django.core.management.base import BaseCommand
from nas.models import *
from billing.models import PeriodicLog

import importlib


class Command(BaseCommand):
    args = ''
    help = 'Firewall setup'


    def handle(self, *args, **options):
        for fire in Firewall.objects.filter(nas__active=True):
            try:
                firewall_module = importlib.import_module('nas.lib.' + fire.kind)
                if hasattr(firewall_module, 'Firewall'):
                    firewall_obj = firewall_module.Firewall(fire.nas)
                    ok = firewall_obj.sync_all()
                    if not ok:
                        PeriodicLog.log("Firewall {} error! ({})".format(fire.nas, fire.nas.ssh_error))
                    del firewall_obj
                del firewall_module
            except ImportError as error:
                print error.message, error.args
                print "Firewall type {} not found".format(fire.kind)
                return None




