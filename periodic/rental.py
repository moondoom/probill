#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import default_periodic
from probill.billing.models import *
import sys
import datetime
from settings import *

def main():
    date = None
    if len(sys.argv) > 1:
        try:
            date = datetime.datetime.strptime(sys.argv[1],'%Y-%m-%d')
        except :
            print u'Неверные формат даты'
            return 0
    msg,code = Tariff.doPeriodRental(date=date)
    PeriodicLog.log(msg,code=code)
    if DEBUG:
        print msg, code

if __name__=="__main__":
    main()

