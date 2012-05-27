#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#System import
import os
import hashlib

# Django import
from django.core.exceptions import ObjectDoesNotExist

#Billing import
from default_periodic import settings
from probill.nas.models import *
from probill.billing.models import PeriodicLog,Account


def main():
    try:
        nas = NasServer.objects.get(id=settings.LOCAL_NAS_ID)
    except ObjectDoesNotExist:
        PeriodicLog.log('Неудалось найти локального NAS сервера c id = 1 Выполнение останволенно',code=100)
        exit(1)
    new_config = ''
    local_subnet = []
    for d_server in nas.dhcpserver_set.all()[0]:
        new_config += configHead(d_server)
        for d_subnet in DHCPServer.dhcpsubnet_set.all():
            new_config += netConfig(d_subnet)
            local_subnet.append(d_subnet.subnet)
    for subnet in local_subnet:
        for account in Account.objects.filter(ip__in=subnet).exclude(mac=None):
            new_config += hostConfig(account)

    old_config = open('/usr/local/etc/dhcpd.conf','r').read()
    if hashlib.md5.new(old_config).digest() <>  hashlib.md5.new(new_config).digest():
        open('/usr/local/etc/dhcpd.conf','w').write(old_config)
        if checkConfig():
            if settings.DEBUG:
                PeriodicLog.log('New dhcp config check ok. Restarting dhcpd.')
            print os.popen('/usr/local/etc/rc.d/isc-dhcpd restart').read()
        else:
            PeriodicLog.log('New dhcp config check fail!!!! Restor old config.')
            open('/usr/local/etc/dhcpd.conf','w').write(old_config)


def checkConfig():
    test1,test2,test3 = os.popen3('dhcpd -t')
    test = test3.read()
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
    """ % (dhcp_subnet.subnet.network,dhcp_subnet.subnet.netmask,dhcp_subnet.default_router)


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
