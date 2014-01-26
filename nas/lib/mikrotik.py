# -*- coding: utf-8 -*-

from settings import *
from nas.models import *
import re
from rosapi import Core

class Firewall:
    address_list_name = "PROBILL_USERS"
    address_list_name_nat = "PROBILL_USERS_NAT_{}"
    qos_re = re.compile(r'(?ms).*?(\d+)\s*;;;.*?name="([^"]*)"\s*target=(\S*).*?max-limit=([^/]*)/(\S*).*?')
    access_re = re.compile(r'(\d+)\s+(\S*)\s+([\.\da-f:]+)\s+')
    dhcp_re = re.compile(r'(\d+)\s+([\.\da-f:]+)\s+([\dA-Fa-f:]+)\s+')

    def __init__(self, nas):
        self.nas = nas
        self.api = Core(str(self.nas.mng_ip),DEBUG=False)
        self.api.login(self.nas.username, self.nas.password)

    def sync_access(self):
        print "ACCESS"
        accounts = []
        for account in self.nas.get_accounts_query(active=True, tariff__isnull=False):
            accounts.append(account)
        self.sync_table(accounts, self.address_list_name)

    def sync_nat(self):
        print "NAT"
        account_table, up_link_table = self.nas.get_up_link_table()
        for up_link in up_link_table:
            self.sync_table(account_table[up_link.id], self.address_list_name_nat.format(up_link.ipfw_nat_id))

    def sync_table(self, accounts, list_name):
        query = self.api.talk(['/ip/firewall/address-list/print','?list={}'.format(list_name)])
        mik_response = self.api.response_handler(query)
        mik_table = {}
        for row in mik_response:
            if row['address'] in mik_table:
                mik_table[row['address']].append(row['.id'])
            else:
                mik_table[row['address']] = [row['.id']]
        for account in accounts:
            if str(account.ip) in mik_table:
                mik_table[str(account.ip)].pop()
            else:
                query = self.api.talk(['/ip/firewall/address-list/add',
                                       '=list={}'.format(list_name),
                                       '=address={}'.format(account.ip),])
                mik_response = self.api.response_handler(query)
                print 'Add', account, mik_response
        for ip in mik_table:
            for address_id in mik_table[ip]:
                query = self.api.talk(['/ip/firewall/address-list/remove','=.id={}'.format(address_id)])
                mik_response = self.api.response_handler(query)
                print 'Remove', ip, mik_response, address_id

    def sync_qos(self):
        print "QOS"

        def resolve_mk(x):
            if x.endswith('k'):
                return int(x[:-1])
            elif x.endswith('M'):
                return int(x[:-1])*1024
            else:
                return int(x)/1024

        query = self.api.talk(['/queue/simple/print',
                               '?=comment={}'.format(self.address_list_name)])

        mik_response = self.api.response_handler(query)
        mik_qos_dict = {}
        for row in mik_response:
            mik_qos_dict[row['target'].split('/')[0]] = [
                row['name'],
                resolve_mk(row['max-limit'].split('/')[0]),
                resolve_mk(row['max-limit'].split('/')[1]),
                row['.id']
            ]


        for account in self.nas.get_accounts_query(active=True, tariff__qos_speed__gt=0):
            ip = str(account.ip)
            if ip in mik_qos_dict:
                if mik_qos_dict[ip][1] != mik_qos_dict[ip][2] or \
                    mik_qos_dict[ip][2] != account.tariff.get_speed() or \
                        mik_qos_dict[ip][0] != '{}_{}'.format(self.address_list_name, account.id):
                    query = self.api.talk(['/queue/simple/set',
                                           '=.id={}'.format(mik_qos_dict[ip][3]),
                                           '=name={}_{}'.format(self.address_list_name, account.id),
                                           '=max-limit={0}k/{0}k'.format(account.tariff.get_speed())])
                    mik_response = self.api.response_handler(query)
                    print 'Update', account, mik_response
                del mik_qos_dict[ip]
            else:

                query = self.api.talk(['/queue/simple/add',
                                       '=target={}'.format(ip),
                                       '=comment={}'.format(self.address_list_name),
                                       '=name={}_{}'.format(self.address_list_name, account.id),
                                       '=max-limit={0}k/{0}k'.format(account.tariff.get_speed()),
                                       '=queue=default/default',
                                       '=packet-marks="no-mark"'])
                mik_response = self.api.response_handler(query)
                print 'Add', account, mik_response

        for ip in mik_qos_dict:
            query = self.api.talk(['/queue/simple/remove','=.id={}'.format(mik_qos_dict[ip][3])])
            mik_response = self.api.response_handler(query)
            print 'Remove', ip, mik_qos_dict[ip], mik_response


    def sync_dhcp(self):
        print "DHCP"
        query = self.api.talk(['/ip/dhcp-server/lease/print',
                               '?=dynamic=no'])

        mik_response = self.api.response_handler(query)

        mik_dhcp_dict = {}
        for row in mik_response:
            mik_dhcp_dict[row['address']] = [row['mac-address'].lower(),  row['.id']]
        for account in self.nas.get_accounts_query():
            if account.ip and account.mac:
                ip, mac = str(account.ip), str(account.mac).lower()
                if ip in mik_dhcp_dict:
                    if mac != mik_dhcp_dict[ip][0]:
                        query = self.api.talk(['/ip/dhcp-server/lease/set',
                                               '=.id={}'.format(mik_dhcp_dict[ip][1]),
                                               '=mac-address={}'.format(mac)])
                        mik_response = self.api.response_handler(query)
                        print 'Update', account, mik_response
                    del mik_dhcp_dict[ip]
                else:

                    query = self.api.talk(['/ip/dhcp-server/lease/add',
                                           '=address={}'.format(ip),
                                           '=mac-address={}'.format(mac)])
                    mik_response = self.api.response_handler(query)
                    print 'Add', account, mik_response
        for ip in mik_dhcp_dict:
            query = self.api.talk(['/ip/dhcp-server/lease/remove','=.id={}'.format(mik_dhcp_dict[ip][1])])
            mik_response = self.api.response_handler(query)
            print 'Remove', ip, mik_dhcp_dict[ip], mik_response

    def sync_arp(self):
        pass

    def sync_all(self):
        self.sync_access()
        self.sync_qos()
        #self.sync_arp()
        self.sync_dhcp()
        self.sync_nat()
        return True