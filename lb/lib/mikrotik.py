__author__ = 'animage'

from nas.lib.mikrotik import Firewall as Old
from nas.models import NasServer
from nas.lib.rosapi import Core
from settings import LB_PREF_SRC

class Tariff():

    def __init__(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

class LBAccount():


    def __init__(self, ip, mac, interface, shape, blocked, id):
        self.ip = ip
        self.mac = mac
        self.interface = interface
        self.tariff = Tariff(shape)
        self.blocked = int(blocked)
        self.id = id

    @classmethod
    def query(cls, dictionary,):
        qu = []
        for ip in dictionary:
            qu.append(LBAccount(ip, dictionary[ip][0], dictionary[ip][1], dictionary[ip][2], dictionary[ip][3], dictionary[ip][4]))
        return qu

    def __str__(self):
        return self.ip + ' ' + self.interface

class FakeNas(NasServer):

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super(FakeNas, self).__init__( *args, **kwargs)
        self.query = []
 
    def set_accounts_query(self, query):
        self.query = query

 
    def get_accounts_query(self, **kwargs):
        if 'active' in kwargs:
            if kwargs['active']:
               
                filtered_query = []
                for ac in self.query[:]:
                    print [ac.blocked == 0, ac , ac.blocked , 0]
                    if not ac.blocked:
                        filtered_query.append(ac)
                return filtered_query
        return self.query[:]


class Firewall(Old):
    address_list_name = "LB_USERS"

    def __init__(self, nas_id, vg_dict):
        self.nas = FakeNas.objects.get(id=nas_id)
        self.api = Core(str(self.nas.mng_ip), DEBUG=False)
        self.api.login(self.nas.username, self.nas.password)
        self.vg_dict  = vg_dict
        self.nas.set_accounts_query(LBAccount.query(self.vg_dict))

    def find_interface(self, ip):
        return self.vg_dict[ip][1]

    def sync_route(self):
        print "ROUTE"
        for account in self.nas.get_accounts_query():
            query = self.api.talk(['/ip/route/add',
                                   '=dst-address={}'.format(account.ip),
                                   '=gateway={}'.format(account.interface),
                                   '=pref-src={}'.format(LB_PREF_SRC)])
            mik_response = self.api.response_handler(query)
            print 'Add', account, mik_response


    def sync_all(self):
        self.sync_access()
        self.sync_qos()
        self.sync_dhcp()
        self.sync_route()