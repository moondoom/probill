#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import default_periodic
from settings import *
from probill.nas.models import *
from subprocess import call

EXTERNAL_HOSTS = (
    'ya.ru',
    '8.8.8.8',
    '4.2.2.2',
    'vk.com',
    'mail.ru'
)


def main():

    for up_link in UpLink.objects.filter(nas__id=LOCAL_NAS_ID, enabled=True).order_by('-priority'):
        if call('%s get default' % ROUTE_PATH,shell=True):
            call('%s add default %s' % (ROUTE_PATH, up_link.remote_address),shell=True)
        check_ok = False
        for host in EXTERNAL_HOSTS:
            if not call('%s -qoS %s -W 0.5 -t1 %s' % (PING_PATH, up_link.local_address,host),shell=True):
                check_ok = True
                break
        if check_ok <> up_link.active:
            up_link.active = check_ok
            up_link.save()


if __name__ == "__main__":
    main()
