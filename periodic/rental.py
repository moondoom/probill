#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import default_periodic
from probill.billing.models import *
import sys
import datetime

def main():
    date = None
    if len(sys.argv) > 1:
        try:
            date = datetime.datetime.strptime(sys.argv[1],'%Y-%m-%d')
        except :
            print u'Неверные формат даты'
            return 0
    Tariff.doPeriodRental(date=date)


if __name__=="__main__":
    main()

