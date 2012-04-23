#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import default_periodic
from settings import *
from probill.billing.models import *
import re
from subprocess import Popen,PIPE

class IpfwObject():

    def get(self,command):
        process = Popen([IPFW_PATH, command],stderr=PIPE,stdout=PIPE)
        error = process.stderr.read()
        if DEBUG:
            print [command,error]
        return process.stdout.read()

    def list(self):
        pass

    def rewrite(self,id,arg):
        pass

    def remove(self,id):
        pass

    def add(self,id,arg):
        pass

    def check(self,standard):
        new_rows = standard.keys()
        for id, arg in self.list():
            if id in standard:
                if arg <> standard[id]:
                    self.rewrite(id,standard[id])
                new_rows.remove(id)
            else:
                self.remove(id)
        for id in new_rows:
            self.add(id,standard[id])


class IpfwTable(IpfwObject):
    re_error = re.compile('.*')

    def __init__(self,number):
        self.number = number

    def add(self,net,arg):
        self.get('table %s add %s %s' % (self.number,net,arg))

    def remove(self,net):
        self.get('table %s delete %s' % (self.number,net))

    def rewrite(self,net,arg):
        self.remove(net)
        self.add(net,arg)

    def list(self):
        self.rows = []
        res = self.get('table %s list' % self.number)
        for row in res.splitlines():
            row = row.split(' ')
            self.rows.append([row[0],int(row[1])])
        return self.rows


class IpfwRuleSet(IpfwObject):

    def __init__(self,start,end):
        self.start = start
        self.end = end

    def add(self,rule_num,rule):
        self.get('add %s %s' % (rule_num,rule))

    def remove(self,rule_num):
        self.get('delete %s' % rule_num)

    def rewrite(self,rule_num,rule):
        self.remove(rule_num)
        self.add(rule_num,rule)

    def list(self):
        self.rows = []
        res = self.get('list %s-%s' % (self.start,self.end))
        for row in res.splitlines():
            row = row.split(' ')
            self.rows.append([int(row[0]),' '.join(row[1:])])
        return self.rows

class IpfwPipe(IpfwObject):
    def __init__(self,name,speed=0,create=False):
        self.name = name
        self.speed = speed
        if create:
            self.add()

    def list(self):
        self.rows = []
        text = self.get('pipe show')
        list = re.findall(r'(?sm).*\n(?P<id>\d+):\s*(?P<speed>[\d\.]+)\s(?P<speed_mux>.*)bit/s.*',text)
        for row in list:
            id = int(row[0])
            speed = float(row[1])
            if row[2] == 'M':
                speed *= 1024
            elif row[2] == '':
                speed /= 1024
            self.rows.append([id,speed])
        return self.rows

    def add(self,id,arg):
        self.get('pipe %s config bw %sKbit/s queue 20' % self.name)

    def remove(self,id):
        self.get('pipe %s delete' % self.name)

class IpfwQueue(IpfwObject):

    def list(self):
        self.rows = []
        text = self.get('queue show')
        list = re.findall(r'(?m)q(\d+).*sched\s(\d+)\sweight.*',
                          text)
        for row in list:
            id = int(row[0])
            pipe = int(row[1])
            self.rows.append([id,pipe])
        return self.rows

    def add(self,id,arg):
        if id % 2:
            mask = 'src-ip'
        else:
            mask = 'dst-ip'
        self.get('queue %s config pipe %s queue 20 mask %s 0xffffffff' % (id,arg,mask))

    def remove(self,id):
        self.get('queue %s delete' % id)


def main():
    def car_name(account,qac=0):
        return account.id*1000000 + qac*10
    QOS_TABLE = IPFW_MIN_TABLE + 1
    ipfw_tables = {IPFW_MIN_TABLE:{},QOS_TABLE:{},QOS_TABLE+1:{}}
    ipfw_rules_in = {
        IPFW_START_IN : 'deny ip from not table(%s) to any' % IPFW_MIN_TABLE,
        IPFW_END_IN : 'queue tablearg ip from table(%s) to any' % QOS_TABLE,
        }
    ipfw_rules_out = {
        IPFW_START_OUT : 'deny ip from any to not table(%s)' % IPFW_MIN_TABLE,
        IPFW_END_OUT : 'queue tablearg ip from any to table(%s)' % (QOS_TABLE + 1),
        }
    qos_maps = {}
    account_qos = {}
    table_number = QOS_TABLE + 1
    rule_offset = 0
    qacs = QosAndCost.objects.all().exclude(qos_speed=0)[:100]
    for qac in qacs:
        rule_offset += IPFW_RULE_STEP
        table_number += 2
        qos_maps[qac.id] = table_number
        ipfw_tables[table_number] = {}
        ipfw_tables[table_number+1] = {}
        nets = ','.join([str(f.network) for f in qac.subnets.all()])
        ipfw_rules_in[rule_offset + IPFW_START_IN] = 'queue tablearg ip from table(%s) to %s' % (table_number,nets)
        ipfw_rules_out[rule_offset + IPFW_START_OUT] = 'queue tablearg ip from %s to table(%s)' % (nets,table_number+1)


    for account in Account.objects.filter(active=True):
        ipfw_tables[IPFW_MIN_TABLE][account.CIDR] = 0
        if account.tariff.qos_speed:
            account_qos[car_name(account)] = [account.tariff.bit_speed,account.tariff.bit_speed]
            ipfw_tables[QOS_TABLE][account.CIDR] = car_name(account)
            ipfw_tables[QOS_TABLE+1][account.CIDR] = car_name(account) + 1
        qacs = account.tariff.qac_class.all().exclude(qos_speed=0)
        if qacs:
            for qac in qacs:
                account_qos[car_name(account,qac.id)] = [qac.bit_speed,qac.bit_speed]
                ipfw_tables[qos_maps[qac.id]][account.CIDR] = car_name(account,qac.id)
                ipfw_tables[qos_maps[qac.id]+1][account.CIDR] = car_name(account,qac.id) + 1

    ng_car = NetGraphCar()
    ng_car.check(account_qos)

    for num in ipfw_tables:
        ipfw_table = IpfwTable(num)
        ipfw_table.check(ipfw_tables[num])

    rule_in = IpfwRuleSet(IPFW_START_IN,IPFW_END_IN)
    rule_in.check(ipfw_rules_in)
    rule_out = IpfwRuleSet(IPFW_START_OUT,IPFW_END_OUT)
    rule_out.check(ipfw_rules_out)








if __name__ == '__main__':
    main()
