# -*- coding: utf-8 -*-

from settings import *
from nas.models import *
import re

class Firewall:
    address_list_name = "PROBILL_USERS"
    qos_re = re.compile(r'(?ms).*?(\d+)\s*;;;.*?name="([^"]*)"\s*target=(\S*).*?limit-at=([^/]*)/(\S*).*?')
    access_re = re.compile(r'(\d+)\s+(\S*)\s+([\.\da-f:]+)\s+')
    dhcp_re = re.compile(r'(\d+)\s+([\.\da-f:]+)\s+([\dA-Fa-f:]+)\s+')

    def __init__(self, nas):
        self.nas = nas

    def sync_access(self):
        print "ACCESS"
        stdin, stdout, stderr = self.nas.exec_command("/ip firewall address-list print without-paging "
                                                      "where list={}".format(self.address_list_name))
        mik_table = self.access_re.findall(stdout.read())
        mik_dict = {}
        for row in mik_table:
            mik_dict[row[2]] = row[0]

        for subnet in IPInterface.objects.filter(iface__nas=self.nas):
            for account in Account.objects.filter(active=True, tariff__isnull=False, ip__in=subnet.network):

                if str(account.ip) in mik_dict:
                    del mik_dict[str(account.ip)]
                else:
                    print 'Add', account
                    self.nas.exec_command('/ip firewall address-list '
                                          'add list={} address={}'.format(self.address_list_name, account.ip))
        for ip in mik_dict:
            self.nas.exec_command('/ip firewall address-list remove '
                                  '[find list={} address={}]'.format(self.address_list_name, ip))

    def sync_qos(self):
        print "QOS"

        def resolve_mk(x):
            if x.endswith('k'):
                return int(x[:-1])
            elif x.endswith('M'):
                return int(x[:-1])*1024
            else:
                return int(x)/1024
        stdin, stdout, stderr = self.nas.exec_command('/queue simple print without-paging '
                                                      'where comment={}'.format(self.address_list_name))
        mik_qos_dict = {}
        mik_qos = stdout.read()
        mik_qos = self.qos_re.findall(mik_qos)
        for row in mik_qos:
            mik_qos_dict[row[2].split('/')[0]] = [
                row[0],
                row[1],
                resolve_mk(row[3]),
                resolve_mk(row[4])
            ]

        for subnet in IPInterface.objects.filter(iface__nas=self.nas):
            for account in Account.objects.filter(active=True, tariff__qos_speed__gt=0, ip__in=subnet.network):
                ip = str(account.ip)
                if ip in mik_qos_dict:
                    if mik_qos_dict[ip][2] != mik_qos_dict[ip][3] or \
                        mik_qos_dict[ip][3] != account.tariff.qos_speed or \
                            mik_qos_dict[ip][1] != '{}_{}'.format(self.address_list_name, account.id):
                        self.nas.exec_command('/queue simple set '
                                              '[find comment={0} target={2}/32] '
                                              'name={0}_{1} max-limit={3}k/{3}k'.format(self.address_list_name,
                                                                                        account.id,
                                                                                        ip,
                                                                                        account.tariff.qos_speed))
                    del mik_qos_dict[ip]
                else:
                    print 'Add', ip
                    self.nas.exec_command('/queue simple add '
                                          'comment={0} target={2}/32 queue=default/default '
                                          'name={0}_{1} max-limit={3}k/{3}k'.format(self.address_list_name,
                                                                                     account.id,
                                                                                     ip,
                                                                                     account.tariff.qos_speed))
        for ip in mik_qos_dict:
            self.nas.exec_command('/queue simple remove '
                                  '[find comment={0} target={1}/32] '.format(self.address_list_name, ip))


    def sync_dhcp(self):
        print "DHCP"
        stdin, stdout, stderr = self.nas.exec_command('/ip dhcp-server lease print without-paging where dynamic=no')

        mik_dhcp_dict = {}
        mik_dhcp = stdout.read()
        mik_dhcp = self.dhcp_re.findall(mik_dhcp)
        for row in mik_dhcp:
            mik_dhcp_dict[row[1]] = row[2].lower()
        for subnet in IPInterface.objects.filter(iface__nas=self.nas):
            for account in Account.objects.filter(ip__in=subnet.network):
                if account.ip and account.mac:
                    ip, mac = str(account.ip), str(account.mac).lower()
                    if ip in mik_dhcp_dict:
                        if mac != mik_dhcp_dict[ip]:
                            print "Update", ip, mac
                            self.nas.exec_command('/ip dhcp-server lease set '
                                                  '[find address={}] '
                                                  'mac-address={}'.format(ip, mac))
                        del mik_dhcp_dict[ip]
                    else:
                        print 'Add', ip, mac
                        self.nas.exec_command('/ip dhcp-server lease add '
                                              'address={} mac-address={}'.format(ip, mac))
        for ip in mik_dhcp_dict:
            print "Remove", ip
            self.nas.exec_command('/ip dhcp-server lease remove [find address={}]'.format(ip))

    def sync_arp(self):
        pass

    def sync_all(self):
        self.sync_access()
        self.sync_qos()
        self.sync_arp()
        self.sync_dhcp()
        return True