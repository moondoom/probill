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
                if str(acc.ip) in arp_dict:
                    return True, arp_dict[str(acc.ip)]['mac'] == acc.mac.lower() \
                        and arp_dict[str(acc.ip)]['status'] == 'permanent'
                else:
                    return False, False
            account_ips = []
            for interface in IPInterface.objects.filter(iface__nas=nas):
                for acc in Account.objects.filter(ip__in=interface.network):
                    account_ips.append(str(acc.ip))
                    if not acc.mac:
                        continue
                    has_arp = check_arp(acc)
                    if DEBUG:
                        print acc.ip, acc.mac, has_arp
                    if not has_arp[1]:
                        nas.exec_command(' '.join([SUDO_PATH, 'arp', '-nS', str(acc.ip), acc.mac]))
                    if has_arp[0]:
                        del arp_dict[str(acc.ip)]
            for ip in arp_dict:
                if arp_dict[ip]['status'] == 'permanent' and ip in account_ips:
                    if DEBUG:
                        print 'Delete old mac', ip, arp_dict[ip]
                    nas.exec_command(' '.join([SUDO_PATH, 'arp', '-nd', ip]))


