#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import default_periodic
from settings import *
from probill.billing.models import Account
from probill.nas.models import *
from subprocess import call

def main():
    for nas in NasServer.objects.filter(active=True):
        if nas.id <> LOCAL_NAS_ID:
            ssh = nas.get_ssh()
        else:
            ssh = None

        for iface in IPInterface.objects.filter(iface__nas=nas):
            for acc in  Account.objects.filter(ip__in=iface.network).exclude(mac=''):
                if ssh:
                    ssh.exec_command(' '.join([SUDO_PATH,'arp','-S',str(acc.ip),acc.mac]))
                else:
                    call(['arp', '-S', str(acc.ip), acc.mac])

if __name__ == "__main__":
    main()
