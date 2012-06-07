#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from default_periodic import settings
from probill.billing.models import *
from datetime import datetime
import os, sys, re

def main():
    """
       flow-stat -f 10 -S1300
       # src IPaddr     dst IPaddr       flows                 octets                packets
       #
       1.1.1.1        8.8.8.8               1                       20                      1
       """
    row_split = re.compile(r'\s*')
    raw_traffic = []
    flow_file =  sys.argv[1]
    file_time = datetime.strptime(flow_file.split('/')[-1:][0][:-5],'ft-v05.%Y-%m-%d.%H%M%S')
    try:
        pipe = os.popen( '%s %s/%s | %s -f 10 -S 3' % ( settings.FLOW_CAT,
                                                     settings.FLOW_PATH,
                                                     flow_file,
                                                     settings.FLOW_STAT))
    except :
        PeriodicLog.log('Ошибка открытия файла %s/%s' % (settings.FLOW_PATH,flow_file))
        exit(1)
    if settings.DEBUG:
        PeriodicLog.log('Начало обработки файла %s' % (pipe))
    while 1:
        line = pipe.readline()
        if line:
            if not line.count('#'):
                line = re.split(row_split,line)
                line = [line[0],line[1],float(line[3])]
                if line[2] > 5096:
                    raw_traffic.append(line)
                else:
                    break
        else:
            break
    try:
        Account.process_traffic(raw_traffic,file_time)
    except :
        PeriodicLog.log('Ошибка скрипта: обработки данных netflow %s' % pipe ,code=100)

if __name__=="__main__":
    if len(sys.argv) >= 2:
        main()
