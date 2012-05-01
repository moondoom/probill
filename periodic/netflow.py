#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from default_periodic import settings
from probill.billing.models import *
import os, sys, re

def main():
    row_split = re.compile(r'\s*')
    raw_traffic = []

    flow_file =  sys.argv[1]
    try:
        pipe = os.popen( '%s %s/%s | %s -f 10 -S 3' % ( settings.FLOW_CAT,
                                                     settings.FLOW_PATH,
                                                     flow_file,
                                                     settings.FLOW_STAT))
    except :
        PeriodicLog.log('Ошибка открытия файла %s/%s' % (settings.FLOW_PATH,flow_file))
    if settings.DEBUG:
        PeriodicLog.log('Начало обработки файла %s' % (pipe))
    while 1:
        line = pipe.readline()
        if line:
            if not line.count('#'):
                line = re.split(row_split,line)
                octets = int(line[3])
                if octets > 5096:
                    raw_traffic.append(line)
                else:
                    break
        else:
            break
    try:
        Account.process_traffic(raw_traffic,datetime.now())
    except :
        PeriodicLog.log('Ошибка скрипта: обработки данных netflow %s' % pipe ,code=100)

if __name__=="__main__":
    if len(sys.argv) >= 2:
        main()
