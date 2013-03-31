#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#System import
import os

# Django import
from django.core.exceptions import ObjectDoesNotExist

#Billing import
from default_periodic import settings
from probill.nas.models import *
from probill.billing.models import PeriodicLog,Account
from settings import  *


def main():
    for nas in NasServer.objects.filter(active=True):
        process_nas(nas)

def process_nas(nas):
    new_config = ''
    local_subnet = []
    for d_server in nas.dhcpserver_set.all():
        new_config = configHead(d_server)
        for d_subnet in d_server.dhcpsubnet_set.all():
            new_config += netConfig(d_subnet)
            local_subnet.append(d_subnet.subnet)
    for subnet in local_subnet:
        for account in Account.objects.filter(ip__in=subnet.network).exclude(mac=None):
            new_config += hostConfig(account)

    old_config = nas.open('/usr/local/etc/dhcpd.conf','r').read()
    if old_config <> new_config:
        nas.open('/usr/local/etc/dhcpd.conf','w').write(new_config)
        if checkConfig(nas):
            if settings.DEBUG:
                PeriodicLog.log('New dhcp config check ok. Restarting dhcpd.')
            stdin, stdout, stderr = nas.exec_command(' '.join([SUDO_PATH, '/usr/local/etc/rc.d/isc-dhcpd restart']))
            print stdout.read()
            print stderr.read()
        else:
            PeriodicLog.log('New dhcp config check fail!!!! Restor old config.')
            nas.open('/usr/local/etc/dhcpd.conf','w').write(old_config)


def checkConfig(nas):
    stdin, stdout, stderr = nas.exec_command(' '.join([SUDO_PATH,'dhcpd -t']))
    test = stderr.read()
    if test.find('Configuration file errors') <> -1:
        return False
    else:
        return True

def hostConfig(account):
    return """
host %s {
        hardware ethernet %s;
        fixed-address %s;
}
    """%(account.login,account.mac,account.ip)


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


if __name__=="__main__":
    main()
