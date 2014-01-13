# -*- coding: utf-8 -*-

from settings import *
from probill.billing.models import *
from probill.nas.models import *
import re
from subprocess import Popen,PIPE

class IpfwObject(object):

    def __init__(self, ssh=None, *args, **kwargs):
        self.ssh = ssh

    def get(self, command):
        if self.ssh:
            stdin , stdout ,stderr = self.ssh.exec_command(' '.join([SUDO_PATH, IPFW_PATH,
                                                                     re.sub(r'([()])',r'\\\1',command)]))
        else:
            process = Popen([IPFW_PATH, command], stderr=PIPE, stdout=PIPE)
            stderr = process.stderr
            stdout = process.stdout
        error = stderr.read()
        if DEBUG:
            print [command,error]
        return stdout.read()

    def list(self):
        pass

    def export(self, id, arg):
        return ''

    def rewrite(self, id, arg):
        self.remove(id)
        self.add(id,arg)

    def remove(self, id):
        pass

    def add(self, id, arg):
        self.get(self.export(id,arg))

    def check(self,standard):
        export_list = []
        new_rows = standard.keys()
        for id, arg in self.list():
            if id in standard:
                if DEBUG: print 'Compare: ',[arg,standard[id]]
                if arg <> standard[id]:
                    self.rewrite(id,standard[id])
                new_rows.remove(id)
            else:
                self.remove(id)
        for id in new_rows:
            self.add(id,standard[id])
        for id in standard:
            export_list.append(self.export(id, standard[id]))
        return export_list


class IpfwTable(IpfwObject):
    re_error = re.compile('.*')

    def __init__(self,number, *args, **kwargs):
        super(IpfwTable,self).__init__(*args, **kwargs)
        self.number = number

    def export(self, id, arg):
        return 'table %s add %s %s' % (self.number, id, arg)

    def remove(self, id):
        self.get('table %s delete %s' % (self.number, id))

    def rewrite(self, id, arg):
        self.remove(id)
        self.add(id, arg)

    def list(self):
        self.rows = []
        res = self.get('table %s list' % self.number)
        for row in res.splitlines():
            row = row.split(' ')
            self.rows.append([row[0],int(row[1])])
        return self.rows


class IpfwRuleSet(IpfwObject):

    def __init__(self, start, end, *args, **kwargs):
        super(IpfwRuleSet,self).__init__(*args, **kwargs)
        self.start = start
        self.end = end

    def export(self,id,arg):
        return 'add %s %s' % (id, arg)

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

class IpfwPipes(IpfwObject):

    def list(self):
        self.rows = []
        text = self.get('pipe show')
        list = re.findall(r'(?m)(?P<id>\d+):\s*(?P<speed>[\d\.]+)\s(?P<speed_mux>.*)bit/s.*',text)
        for row in list:
            print row
            id = int(row[0])
            speed = float(row[1])
            if row[2] == 'M':
                speed *= 1000
            elif row[2] == '':
                speed /= 1000
            self.rows.append([id,speed])
        return self.rows


    def export(self, id, arg):
        if id % 2:
            mask = 'src-ip'
        else:
            mask = 'dst-ip'
        return 'pipe %s config bw %sKbit/s queue %s gred 0.002/%s/%s/0.1 mask %s 0xffffffff' % (id,
                                                                                                  arg,
                                                                                                  IPFW_QUEUE_SIZE,
                                                                                                  IPFW_QUEUE_SIZE/2,
                                                                                                  IPFW_QUEUE_SIZE,
                                                                                                  mask)

    def remove(self,id):
        self.get('pipe %s delete' % id)

class IpfwQueues(IpfwObject):

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

    def export(self,id,arg):
        if id % 2:
            mask = 'src-ip'
        else:
            mask = 'dst-ip'
        return 'queue %s config pipe %s weight 50 mask %s 0xffffffff' % (id,arg,mask)

    def remove(self,id):
        self.get('queue %s delete' % id)

class IPFWManager():
    off_line_rules = []
    QOS_TABLE = IPFW_MIN_TABLE + 1
    cursor = IPFW_NAT_START


    def __init__(self, nas):
        self.nas = nas
        self.ipfw_tables = {IPFW_MIN_TABLE:{},
                            self.QOS_TABLE:{},
                            self.QOS_TABLE + 1:{},
                            IPFW_NAT_TABLE:{}}

        self.ipfw_rules_in = {}
        self.ipfw_rules_out = {}
        self.ipfw_rules_nat = {}

        self.init_ssh()

    def sync_rules(self):
        self.ipfw_rules_in = {
            IPFW_END_IN - IPFW_RULE_STEP*3 : 'pipe tablearg ip from table(%s) to any' % self.QOS_TABLE,
            IPFW_END_IN - IPFW_RULE_STEP*2: 'allow ip from table(%s) to any' % IPFW_MIN_TABLE,
            IPFW_END_IN : 'deny ip from any to any',
            }
        self.ipfw_rules_out = {
            IPFW_END_OUT - IPFW_RULE_STEP*3 : 'pipe tablearg ip from any to table(%s)' % (self.QOS_TABLE + 1),
            IPFW_END_OUT - IPFW_RULE_STEP*2: 'allow ip from any to table(%s)' % IPFW_MIN_TABLE,
            IPFW_END_OUT : 'deny ip from any to any',
            }
        if REDIRECT_TO:
            self.ipfw_rules_in[IPFW_END_IN - IPFW_RULE_STEP] = 'fwd {} tcp from any to any dst-port 80'.format(REDIRECT_TO)
            self.ipfw_rules_out[IPFW_END_OUT - IPFW_RULE_STEP] = 'allow tcp from any 80 to any'

    def init_ssh(self):
        if self.nas.id <> LOCAL_NAS_ID:
            self.ssh = self.nas.get_ssh()
            if not self.ssh:
                return False
        else:
            self.ssh = None

    def sync_nat_rules(self):
        self.ipfw_rules_nat[self.cursor] = 'nat tablearg ip from table(%s) to any' % IPFW_NAT_TABLE
        self.cursor += IPFW_RULE_STEP
        for nat in self.nats:
            self.ipfw_rules_nat[self.cursor] = 'nat %s ip from any to %s' % (nat.ipfw_nat_id,nat.local_address)
            self.cursor += IPFW_RULE_STEP
            self.ipfw_rules_nat[self.cursor] = 'fwd %s ip from %s to any' % (nat.remote_address,nat.local_address)
            self.cursor += IPFW_RULE_STEP

    def sync_nat_tables(self):
        account_static_nat = {}
        for nat_rule in UpLinkPolice.objects.filter(nat_address__in=self.active_nat,nat_address__nas=self.nas):
            if nat_rule.accounts:
                for account in nat_rule.accounts.all():
                    account_static_nat[account.id] = nat_rule.nat_address
            if nat_rule.network:
                for account in Account.objects.filter(ip__in=nat_rule.network):
                    account_static_nat[account.id] = nat_rule.nat_address

        # Если нет неодного доступного правила натирования то рубим пользователей! Иначе трафик будет уходить нетуда.
        if self.nat_max_priority > 0:
            nat_choice_length = len(self.nat_priority_table[self.nat_max_priority]) - 1
            nat_choice = 0
            for subnet in IPInterface.objects.filter(iface__nas=self.nas):
                for account in Account.objects.filter(active=True,ip__in=subnet.network):
                    self.ipfw_tables[IPFW_MIN_TABLE][account.CIDR] = 0
                    if account.id in account_static_nat:
                        nat_id = account_static_nat[account.id].ipfw_nat_id
                    else:
                        if nat_choice > nat_choice_length:
                            nat_choice = 0
                        nat_id = self.nat_priority_table[self.nat_max_priority][nat_choice].ipfw_nat_id
                        nat_choice += 1
                    self.ipfw_tables[IPFW_NAT_TABLE][account.CIDR] = nat_id

    def calc_nat_priority(self):
        for nat in self.nats:
            if nat.active:
                self.active_nat.append(nat.id)
                if nat.priority > self.nat_max_priority:
                    self.nat_max_priority = nat.priority
                if nat.priority not in self.nat_priority_table:
                    self.nat_priority_table[nat.priority] = [nat]
                else:
                    self.nat_priority_table[nat.priority].append(nat)


    def sync_nat(self):
        # NAT section
        self.nats = UpLink.objects.filter(enabled=True, nas=self.nas)
        self.cursor += IPFW_RULE_STEP
        self.nat_priority_table = {}
        self.nat_max_priority = 0
        self.active_nat = []
        self.calc_nat_priority()
        self.sync_nat_rules()
        self.sync_nat_tables()



    def sync_qos(self):
        queue_map = {}
        queue_map_id = 1
        for subnet in IPInterface.objects.filter(iface__nas=self.nas):
            for account in Account.objects.filter(active=True, tariff__isnull=False, ip__in=subnet.network):
                if account.tariff.qos_speed:
                    speed_id = str(account.tariff.get_speed())
                    if speed_id not in queue_map:
                        queue_map[speed_id] = queue_map_id
                        queue_map_id += 2
                    self.ipfw_tables[self.QOS_TABLE][account.CIDR] = queue_map[speed_id]
                    self.ipfw_tables[self.QOS_TABLE+1][account.CIDR] = queue_map[speed_id]+1

        pipe_std = {}
        for x in queue_map:
            pipe_std[queue_map[x]] = int(x.split('_')[0])
            pipe_std[queue_map[x]+1] = int(x.split('_')[0])


        Pipes = IpfwPipes(ssh=self.ssh)
        self.off_line_rules += Pipes.check(pipe_std)

    def sync_all(self):
        self.sync_rules()
        self.sync_qos()
        self.sync_nat()
        for num in self.ipfw_tables:
            ipfw_table = IpfwTable(num,ssh=self.ssh)
            self.off_line_rules += ipfw_table.check(self.ipfw_tables[num])

        rule_in = IpfwRuleSet(IPFW_START_IN,IPFW_END_IN,ssh=self.ssh)
        self.off_line_rules += rule_in.check(self.ipfw_rules_in)
        rule_out = IpfwRuleSet(IPFW_START_OUT,IPFW_END_OUT,ssh=self.ssh)
        self.off_line_rules += rule_out.check(self.ipfw_rules_out)
        rule_nat = IpfwRuleSet(IPFW_NAT_START,IPFW_NAT_END,ssh=self.ssh)
        self.off_line_rules += rule_nat.check(self.ipfw_rules_nat)
        off_line_file = self.nas.open(IPFW_INCLUDE,'wb')
        off_line_file.write('\n'.join(self.off_line_rules) + '\n')
        off_line_file.close()
        return True

def process_nas(nas):
    ipfw = IPFWManager(nas)
    ipfw.sync_all()