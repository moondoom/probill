from django.core.management.base import BaseCommand
from nas.models import *

import importlib


class Command(BaseCommand):
    args = ''
    help = 'Firewall setup'


    def handle(self, *args, **options):
        for nas in NasServer.objects.filter(active=True):
            try:
                firewall_module = importlib.import_module('nas.lib.' + nas.type)
                if hasattr(firewall_module, 'Firewall'):
                    firewall_class = firewall_module.Firewall
                    firewall_obj = firewall_class(nas)
                    firewall_obj.sync_all()
                    del firewall_obj, firewall_class
                del firewall_module
            except ImportError as error:
                print error.message, error.args
                print "Firewall type {} not found".format(nas.type)
                return None




