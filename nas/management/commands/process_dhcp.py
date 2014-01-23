from django.core.management.base import BaseCommand
from nas.models import *
from datetime import datetime,timedelta
from settings import *
import re


class Command(BaseCommand):
    args = ''
    help = 'Firewall setup'

    def handle(self, *args, **options):
        for dhcp_serv in DHCPServer.objects.filter(nas__active=True):
            process_dhcp(dhcp_serv)

def process_dhcp(d_server):
    local_subnet = []
    new_config = configHead(d_server)
    for d_subnet in d_server.dhcpsubnet_set.all():
        new_config += netConfig(d_subnet)
        local_subnet.append(d_subnet.subnet)
    for subnet in local_subnet:
        for account in Account.objects.filter(ip__in=subnet.network, mac__isnull=False):
            if account.mac and account.ip:
                new_config += hostConfig(account)
    print new_config
    old_config = d_server.nas.open('/usr/local/etc/dhcpd.conf', 'r').read()
    if old_config != new_config:
        d_server.nas.open('/usr/local/etc/dhcpd.conf', 'w').write(new_config)
        if checkConfig(d_server.nas):
            stdin, stdout, stderr = d_server.nas.exec_command(' '.join([SUDO_PATH,
                                                                        '/usr/local/etc/rc.d/isc-dhcpd restart']))
            print stdout.read()
            print stderr.read()
        else:
            d_server.nas.open('/usr/local/etc/dhcpd.conf', 'w').write(old_config)


def checkConfig(nas):
    stdin, stdout, stderr = nas.exec_command(' '.join([SUDO_PATH, 'dhcpd -t']))
    test = stderr.read()
    if test.find('Configuration file errors') != -1:
        return False
    else:
        return True


def hostConfig(account):
    if account.login:
        login = account.login
    else:
        login = '{}-{}'.format(account.subscriber.login, str(account.ip).replace('.', '-'))
    return """
host %s {
        hardware ethernet %s;
        fixed-address %s;
}
    """ % (login, account.mac, account.ip)


def netConfig (dhcp_subnet):
    return """
subnet %s netmask %s {
        authoritative;
        max-lease-time 86400;
        option routers %s;
}
    """ % (dhcp_subnet.subnet.network.network,dhcp_subnet.subnet.network.netmask,dhcp_subnet.default_router)


def configHead(dhcp_server):
    return """
option domain-name-servers %s, %s;
ddns-update-style none;
default-lease-time 86400;
""" % (dhcp_server.dns_first,dhcp_server.dns_second)



def mac2mac(mac):
    tmp=[]
    for x in range(0,11,2):
        tmp.append(mac[x]+mac[x+1])
    return ':'.join(tmp)
