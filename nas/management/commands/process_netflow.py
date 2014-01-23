from django.core.management.base import BaseCommand
from nas.models import *
from datetime import datetime,timedelta
from settings import *
import re


class Command(BaseCommand):
    args = ''
    help = 'Firewall setup'

    def handle(self, *args, **options):
        for nf_pro in NetFlowProcessor.objects.filter(nas__active=True):
            row_split = re.compile(r'\s*')
            flow_files = []
            for days in range(0, 3):
                flow_dir = (datetime.now() - timedelta(days=days)).strftime(nf_pro.flow_source_path)
                try:
                    flow_files += [[flow_dir, f] for f in nf_pro.nas.listdir(flow_dir) if f.startswith('ft')]
                except IOError:
                    pass
                except OSError:
                    pass
            old_files = NetFlowSource.objects.filter(nas=nf_pro.nas,
                                                     file_time__gt=(datetime.now() - timedelta(days=3))).values_list('file_name')
            old_files = [f[0] for f in old_files]
            for flow_file in flow_files:
                if flow_file[1] not in old_files:
                    raw_traffic = []
                    file_time = datetime.strptime(flow_file[1][:-5], nf_pro.flow_source_time_mask)
                    try:
                        stdin, stdout, stderr = nf_pro.nas.exec_command(
                            '{0:>s}/flow-cat {1:>s}/{2:>s} | {0:>s}/flow-stat -f 10 -S 3'.format(nf_pro.flow_tools_path,
                                                                                                 flow_file[0],
                                                                                                 flow_file[1]))
                    except Exception as error:
                        stdin, stdout, stderr = None, None, None
                        exit(1)
                    while 1:
                        line = stdout.readline()
                        if line:

                            if not line.count('#'):
                                line = re.split(row_split, line)
                                line = [line[0], line[1], float(line[3])]
                                if line[2] > 5096:
                                    raw_traffic.append(line)
                                else:
                                    break
                        else:
                            break
                    try:
                        if DEBUG:
                            print flow_file
                        Account.process_traffic(raw_traffic, file_time)
                        NetFlowSource(nas=nf_pro.nas,
                            file_dir=flow_file[0],
                            file_name=flow_file[1],
                            file_time=file_time).save()
                    except Exception as error:
                        print error.args, error.message





