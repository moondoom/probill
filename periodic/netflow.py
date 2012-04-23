#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from default_periodic import settings
from probill.billing.models import *
import os, sys, re

def main():
    row_split = re.compile(r'\s*')
    raw_traffic = []
    if sys.stdin.isatty():
        flow_file =  sys.argv[1]
        pipe = os.popen( '%s %s | %s -f 10 -S 3' % ( settings.FLOW_CAT,
                                                     flow_file,
                                                     settings.FLOW_STAT))
    else:
        pipe = sys.stdin

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
    Account.process_traffic(raw_traffic,datetime.now())

if __name__=="__main__":
    if len(sys.argv) >= 2 or not sys.stdin.isatty():
        main()
