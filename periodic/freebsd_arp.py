#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import default_periodic
from settings import *
from probill.billing.models import Account
from probill.nas.models import *
from subprocess import call

def main():
    Nas = NasServer.objects.get(id=LOCAL_NAS_ID)
    for iface in IPInterface.objects.filter(iface__nas=Nas):
        for acc in  Account.objects.filter(ip__in=iface.network).exclude(mac=''):
            call(['arp','-S',str(acc.ip), acc.mac])

if __name__ == "__main__":
    main()
