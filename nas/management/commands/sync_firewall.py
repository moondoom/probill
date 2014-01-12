from django.core.management.base import BaseCommand
from nas.models import *
from nas.lib.freebsd_ipfw import process_nas
from nas.lib.freebsd_ipfw_no_fwd import process_nas as process_nas_no_fwd



class Command(BaseCommand):
    args = ''
    help = 'Firewall setup'

    def freebsd_ipfw_firewall(self, nas):
        return process_nas(nas)

    def freebsd_ipfw_no_fwd_firewall(self, nas):
        return process_nas_no_fwd(nas)

    def linux_ipt_tc_firewall(self, nas):
        return None



    def handle(self, *args, **options):
        for nas in NasServer.objects.filter(active=True):
            try:
                method = getattr(self,nas.type + '_firewall')
                print method
                print method(nas)
            except Exception as error:
                print error.message , error.args
                print "Firewall type {} not found".format(nas.type)
                return None



