from django.core.management.base import BaseCommand
from probill.settings import *
from nas.models import *
from subprocess import call


class Command(BaseCommand):
    args = ''
    help = 'Delete selected object'

    def handle(self, *args, **options):
        for nas in NasServer.objects.filter(active=True):
            stdin, stdout, stderr = nas.exec_command(' '.join([SUDO_PATH, 'arp', '-an']))
            arp_table = stdout.read()
            arp_table = [f.split(' ') for f in arp_table.splitlines()]
            arp_dict = {}
            for arp in arp_table:
                arp_dict[arp[1][1:][:-1]] = {'mac': arp[3], 'status': arp[6]}

            def check_arp(acc):
                if acc.ip in arp_dict:
                    return arp_dict[acc.ip]['mac'] == acc.mac \
                        and arp_dict[acc.ip]['status'] == 'permanent'
                return False

            for interface in IPInterface.objects.filter(iface__nas=nas):
                for acc in Account.objects.filter(ip__in=interface.network).exclude(mac=''):
                    if check_arp(acc):
                        nas.exec_command(' '.join([SUDO_PATH, 'arp', '-nS', str(acc.ip), acc.mac]))
                    del arp_dict[acc.ip]
            for ip in arp_dict:
                if arp_dict[ip]['status'] == 'permanent':
                    nas.exec_command(' '.join([SUDO_PATH, 'arp', '-nd', ip]))


