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

class NetGraphObject():

    def get(self,command):
        process = Popen([NETGRAPH_PATH, '-f-'],stderr=PIPE,stdout=PIPE,stdin=PIPE)
        print >> process.stdin, command
        process.stdin.close()
        error = process.stderr.read()
        if DEBUG:
            print command
            print error
        return process.stdout.read()

class NetGraphCarNode(NetGraphObject):

    def __init__(self,name,up_speed=0,down_speed=0,create=False):
        self.name = name
        self.up_speed = up_speed
        self.down_speed = down_speed
        if create:
            self.add()

    def getConfig(self):
        text = self.get('msg %s: getconf' % self.name)
        regex = re.match(r'(?s).*upstream={.*cir=(?P<upcir>\d*).*downstream.*cir=(?P<downcir>\d*).*',text)
        self.up_speed = int(regex.group('upcir'))
        self.down_speed = int(regex.group('downcir'))
        return [self.up_speed, self.down_speed]

    def setConfig(self):
        up_speed = self.up_speed
        up_burst = self.up_speed*0.125
        down_speed = self.down_speed
        down_burst = self.down_speed*0.125
        msg = ' '.join(['msg %s: setconf' % self.name,
                        '{ upstream={ cbs=%d ebs=%d cir=%d' % (up_burst,up_burst,up_speed),
                        'greenAction=1 yellowAction=1 redAction=2 mode=3 }',
                        'downstream={ cbs=%d ebs=%d cir=%d' % (down_burst,down_burst,down_speed),
                        'greenAction=1 yellowAction=1 redAction=2 mode=3 }}',
                        ])
        self.get(msg)

    def add(self):
        msg = ['mkpeer ipfw: car %s upper' % self.name,
               'name ipfw:%s %s' % (self.name,self.name),
               'connect %s: ipfw: lower %s' % (self.name,self.name+1)]
        self.get('\n'.join(msg))
        self.setConfig()

    def remove(self):
        self.get('shutdown %s:' % self.name)


    def check(self,up_speed,down_speed):
        self.getConfig()
        if up_speed <> self.up_speed or down_speed <> self.down_speed:
            self.up_speed = up_speed
            self.down_speed = down_speed
            self.setConfig()

class NetGraphCar(NetGraphObject):

    def list(self):
        self.nodes = {}
        text = self.get('list')
        for row in text.splitlines():
            if row.count('Type: car'):
                row = re.split(r'\s+',row)
                self.nodes[int(row[2])] = NetGraphCarNode(row[2])
        return self.nodes

    def check(self,standard):
        new_nodes = standard.keys()
        for node in self.list():
            if  node in standard:
                self.nodes[node].check(*standard[node])
                new_nodes.remove(node)
            else:
                self.nodes[node].remove()
        for node_name in new_nodes:
            NetGraphCarNode(node_name,
                up_speed=standard[node_name][0],
                down_speed=standard[node_name][1],
                create=True
            )




def main():
    def car_name(account,qac=0):
        return account.id*1000000 + qac*10
    QOS_TABLE = IPFW_MIN_TABLE + 1
    ipfw_tables = {IPFW_MIN_TABLE:{},QOS_TABLE:{},QOS_TABLE+1:{}}
    ipfw_rules_in = {
        IPFW_START_IN : 'deny ip from not table(%s) to any' % IPFW_MIN_TABLE,
        IPFW_END_IN : 'netgraph tablearg ip from table(%s) to any' % QOS_TABLE,
        }
    ipfw_rules_out = {
        IPFW_START_OUT : 'deny ip from any to not table(%s)' % IPFW_MIN_TABLE,
        IPFW_END_OUT : 'netgraph tablearg ip from any to table(%s)' % (QOS_TABLE + 1),
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
        ipfw_rules_in[rule_offset + IPFW_START_IN] = 'netgraph tablearg ip from table(%s) to %s' % (table_number,nets)
        ipfw_rules_out[rule_offset + IPFW_START_OUT] = 'netgraph tablearg ip from %s to table(%s)' % (nets,table_number+1)


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
