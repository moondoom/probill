# -*- coding: utf-8 -*-

from settings import *
from nas.models import *
from rosapi import Core
from billing.models import PeriodicLog
from ipaddr import IPAddress

class Firewall:
    address_list_name = "PROBILL_USERS"
    address_blacklist_name = "PROBILL_BLACKLIST"
    address_list_name_nat = "PROBILL_USERS_NAT_{}"


    def __init__(self, nas):
        self.nas = nas
        self.api = Core(str(self.nas.mng_ip),DEBUG=False)
        self.api.login(self.nas.username, self.nas.password)
        self.interface = {}
        for interface in NetworkInterface.objects.filter(nas=self.nas):
            self.interface[interface.name] = []
            for net in IPInterface.objects.filter(iface=interface):
                self.interface[interface.name].append(net.network)

    def find_interface(self, account):
        if account.interface:
            return account.interface
        for interface in self.interface:
            for net in self.interface[interface]:
                if account.ip in net:
                    return interface
        return 'all'

    def sync_access(self):
        print "ACCESS"
        accounts = []
        for account in self.nas.get_accounts_query(active=True, tariff__isnull=False):
            accounts.append(account)
        self.sync_table(accounts, self.address_list_name)

    def sync_nat(self):
        print "NAT"
        account_up_link = self.nas.get_up_link_table()
        up_link_account = {}
        for account in account_up_link:
            if  account_up_link[account] in up_link_account:
                up_link_account[account_up_link[account]].append(account)
            else:
                up_link_account[account_up_link[account]] = [account]
        # SYNC TABLE
        good_id = []
        for up_link in up_link_account:
            good_id.append(up_link.ipfw_nat_id)
            self.sync_table(up_link_account[up_link], self.address_list_name_nat.format(up_link.ipfw_nat_id))
        # REMOVE UNUSED TABLE
        self.remove_bad_table(self.address_list_name_nat, good_id)

    def remove_bad_table(self, list_template, good_id):
        query = self.api.talk(['/ip/firewall/address-list/print',])
        mik_response = self.api.response_handler(query)
        list_prefix = list_template.format('')
        good_list = [list_template.format(f) for f in good_id]
        for row in mik_response:
            if row['list'].startswith(list_prefix) and row['list'] not in good_list:
                query = self.api.talk(['/ip/firewall/address-list/remove', '=.id={}'.format(row['.id'])])
                mik_response = self.api.response_handler(query)
                print 'Remove', row['list'], row['address'], mik_response


    def sync_blacklist(self):
        print "BLACKLIST"
        blacklist = []
        for ip in BlackListByIP.objects.all():
            blacklist.append(ip)
        self.sync_table(blacklist, self.address_blacklist_name)

    def sync_table(self, accounts, list_name):
        query = self.api.talk(['/ip/firewall/address-list/print', '?list={}'.format(list_name)])
        mik_response = self.api.response_handler(query)
        mik_table = {}
        for row in mik_response:
            if row['address'] in mik_table:
                mik_table[row['address']].append(row['.id'])
            else:
                mik_table[row['address']] = [row['.id']]
        for account in accounts:
            ip = str(account.ip)
            if ip.endswith('/32'):
                ip = ip[:-3]
            if ip in mik_table:
                if mik_table[ip]:
                    mik_table[ip].pop()
                else:
                    PeriodicLog.log('Script PROCESS_FIREWALL_MIKROTIK, posible ip double {}'.format(account.ip),
                                    code=10)
            else:
                query = self.api.talk(['/ip/firewall/address-list/add',
                                       '=list={}'.format(list_name),
                                       '=address={}'.format(ip),])
                mik_response = self.api.response_handler(query)
                print 'Add', account, mik_response
        for ip in mik_table:
            for address_id in mik_table[ip]:
                query = self.api.talk(['/ip/firewall/address-list/remove', '=.id={}'.format(address_id)])
                mik_response = self.api.response_handler(query)
                print 'Remove', ip, mik_response, address_id

    def sync_qos(self):
        print "QOS"

        def resolve_mk(x):
            if x.endswith('k'):
                return int(x[:-1])
            elif x.endswith('M'):
                return int(x[:-1]) * 1024
            else:
                return int(x) / 1024

        query = self.api.talk(['/queue/simple/print',
                               '?=comment={}'.format(self.address_list_name)])

        mik_response = self.api.response_handler(query)
        mik_qos_dict = {}
        for row in mik_response:
            account_id = int(row['name'].split('_')[2])
            mik_qos_dict[account_id] = [
                row['target'].split('/')[0],
                resolve_mk(row['max-limit'].split('/')[0]),
                resolve_mk(row['max-limit'].split('/')[1]),
                row['.id'],
                row['packet-marks']
            ]

        for account in self.nas.get_accounts_query(active=True, tariff__qos_speed__gt=0):
            ip = str(account.ip)
            packet_marks_push = ",".join(['"{}"'.format(f) for f in SQ_PACKET_MARKS])
            packet_marks_pull = ",".join(SQ_PACKET_MARKS)

            if account.id in mik_qos_dict:
                if mik_qos_dict[account.id][1] != mik_qos_dict[account.id][2] or \
                    mik_qos_dict[account.id][2] != account.tariff.get_speed() or \
                        mik_qos_dict[account.id][0] != ip or mik_qos_dict[account.id][4] != packet_marks_pull:
                    query = self.api.talk(['/queue/simple/set',
                                           '=.id={}'.format(mik_qos_dict[account.id][3]),
                                           '=target={}'.format(ip),
                                           '=max-limit={0}k/{0}k'.format(account.tariff.get_speed()),
                                           '=packet-marks={}'.format(packet_marks_push)])
                    mik_response = self.api.response_handler(query)
                    print 'Update', account, mik_qos_dict[account.id], account.tariff.get_speed()
                del mik_qos_dict[account.id]
            else:

                query = self.api.talk(['/queue/simple/add',
                                       '=target={}'.format(ip),
                                       '=comment={}'.format(self.address_list_name),
                                       '=name={}_{}'.format(self.address_list_name, account.id),
                                       '=max-limit={0}k/{0}k'.format(account.tariff.get_speed()),
                                       '=queue=hotspot-default/hotspot-default',
                                       '=packet-marks={}'.format(packet_marks_push)])
                mik_response = self.api.response_handler(query)
                print 'Add', account, mik_response

        for account_id in mik_qos_dict:
            query = self.api.talk(['/queue/simple/remove', '=.id={}'.format(mik_qos_dict[account_id][3])])
            mik_response = self.api.response_handler(query)
            print 'Remove', mik_qos_dict[account_id], mik_response

    def sync_qos_new(self):
        qos = {}
        for account in self.nas.get_accounts_query(tariff__qos_speed__gt=0):
            speed = account.tariff.get_speed()
            if speed in qos:
                qos[account.tariff.get_speed()].append(account)
            else:
                qos[account.tariff.get_speed()] = [account]
        for speed in qos:
            self.sync_table(qos[speed], '{}_QOS_{}'.format(self.address_list_name, speed))
        self.remove_bad_table('{}_QOS_{}'.format(self.address_list_name, '{}'), qos.keys())

    def sync_dhcp(self):
        print "DHCP"
        query = self.api.talk(['/ip/dhcp-server/lease/print',
                               '=.proplist=address,mac-address,server,.id',
                               '?=dynamic=no',
                               '?=comment={}'.format(self.address_list_name)])

        mik_response = self.api.response_handler(query)
        
        mik_dhcp_dict = {}
        for row in mik_response:
            if 'server' in row:
                mik_dhcp_dict[row['address']] = [row['mac-address'].lower(),  row['.id'], row['server']]
            else:
                mik_dhcp_dict[row['address']] = [row['mac-address'].lower(),  row['.id'], 'all']
        for account in self.nas.get_accounts_query():
            if account.ip and account.mac:
                ip, mac = str(account.ip), str(account.mac).lower()
                interface = self.find_interface(account)
                if ip in mik_dhcp_dict:
                    if mac != mik_dhcp_dict[ip][0] or interface != mik_dhcp_dict[ip][2]:
                        query = self.api.talk(['/ip/dhcp-server/lease/set',
                                               '=.id={}'.format(mik_dhcp_dict[ip][1]),
                                               '=mac-address={}'.format(mac),
                                               '=server={}'.format(interface)])
                        mik_response = self.api.response_handler(query)
                        print 'Update', account, mik_response
                    del mik_dhcp_dict[ip]
                else:
                    query = self.api.talk(['/ip/dhcp-server/lease/add',
                                           '=address={}'.format(ip),
                                           '=mac-address={}'.format(mac),
                                           '=server={}'.format(interface),
                                           '=comment={}'.format(self.address_list_name)])
                    mik_response = self.api.response_handler(query)
                    print 'Add', account, mik_response
        for ip in mik_dhcp_dict:
            query = self.api.talk(['/ip/dhcp-server/lease/remove', '=.id={}'.format(mik_dhcp_dict[ip][1])])
            mik_response = self.api.response_handler(query)
            print 'Remove', ip, mik_dhcp_dict[ip], mik_response

    def sync_route(self):
        print "ROUTE"
        query = self.api.talk(['/ip/route/print',
                               '?=comment={}'.format(self.address_list_name)])
        mik_response = self.api.response_handler(query)
        mik_rt = {}
        for row in mik_response:
            mik_rt[row['dst-address'].split('/')[0]] = [
                row['gateway'],
                row['pref-src'],
                row['.id']
            ]
        query = self.nas.get_accounts_query()
        query = query.exclude(Q(interface__isnull=True) | Q(interface=''))
        for account in query:
            ip = str(account.ip)
            if ip in mik_rt:
                if mik_rt[ip][0] != account.interface or mik_rt[ip][1] != LB_PREF_SRC:
                    query = self.api.talk(['/ip/route/set',
                                           '=.id={}'.format(mik_rt[ip][2]),
                                           '=gateway={}'.format(account.interface),
                                           '=pref-src={}'.format(LB_PREF_SRC)])
                    mik_response = self.api.response_handler(query)
                    print 'UPDATE', account, mik_response
                del mik_rt[ip]
            else:
                query = self.api.talk(['/ip/route/add',
                                       '=dst-address={}'.format(account.ip),
                                       '=gateway={}'.format(account.interface),
                                       '=pref-src={}'.format(LB_PREF_SRC),
                                       '=comment={}'.format(self.address_list_name)])
                mik_response = self.api.response_handler(query)
                print 'Add', account, mik_response
        for ip in mik_rt:
            query = self.api.talk(['/ip/route/remove','=.id={}'.format(mik_rt[ip][2])])
            mik_response = self.api.response_handler(query)
            print 'Remove', ip, mik_rt[ip], mik_response

    def sync_arp(self):
        pass

    def sync_all(self):
        self.sync_access()
        if NEW_QOS:
            self.sync_qos_new()
        else:
            self.sync_qos()
        #self.sync_arp()


        self.sync_route()
        self.sync_dhcp()
        self.sync_nat()
        self.sync_blacklist()
        return True
