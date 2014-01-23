#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from default_periodic import settings
from probill.billing.models import *
from probill.nas.models import *
from datetime import datetime,timedelta
from settings import *
import re

def process_nas(nas):
    """
       flow-stat -f 10 -S1300
       # src IPaddr     dst IPaddr       flows                 octets                packets
       #
       1.1.1.1        8.8.8.8               1                       20                      1
       """
    row_split = re.compile(r'\s*')

    flow_files = []
    for days in range(0, 3):
        flow_dir = (datetime.now() - timedelta(days=days)).strftime(settings.FLOW_PATH)
        try:
            flow_files += [[flow_dir, f] for f in nas.listdir(flow_dir) if f.startswith('ft')]
        except IOError:
            pass
        except OSError:
            pass
    old_files = NetFlowSource.objects.filter(nas=nas, file_time__gt=(datetime.now() - timedelta(days=3))).values_list('file_name')
    old_files = [f[0] for f in old_files]
    for flow_file in flow_files:
        if flow_file[1] not in old_files:
            raw_traffic = []
            file_time = datetime.strptime(flow_file[1][:-5],'ft-v05.%Y-%m-%d.%H%M%S')
            try:
                stdin, stdout, stderr = nas.exec_command(
                    '{0:>s} {1:>s}/{2:>s} | {3:>s} -f 10 -S 3'.format(settings.FLOW_CAT,
                        flow_file[0],
                        flow_file[1],
                        settings.FLOW_STAT))
            except Exception as error:
                PeriodicLog.log('Ошибка открытия файла %s/%s %s' % (flow_file[0], flow_file[1], error.message))
                stdin, stdout, stderr = None, None, None
                exit(1)
            if settings.DEBUG:
                PeriodicLog.log('Начало обработки файла {0:>s}'.format(flow_file))
            while 1:
                line = stdout.readline()
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
                if DEBUG:
                    print flow_file
                Account.process_traffic(raw_traffic,file_time)
                NetFlowSource(nas=nas,
                    file_dir=flow_file[0],
                    file_name=flow_file[1],
                    file_time=file_time).save()
            except Exception as error:
                print error.args, error.message
                PeriodicLog.log('Ошибка скрипта: обработки данных netflow {0:>s}'.format(flow_file),code=100)

def main():
    for nas in NasServer.objects.filter(active=True):
        rez = process_nas(nas)
        if DEBUG:
            print rez


if __name__=="__main__":
    main()
