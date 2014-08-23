# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from probill.lib.networks import IPAddressField,IPNetworkField
from probill.billing.models import Account
import os
import operator
from itertools import cycle


class NasServer(models.Model):
    #STATIC
    ssh_error = None
    ssh = None

    name = models.CharField(max_length=50)
    mng_ip = IPAddressField()
    username = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    active = models.BooleanField(default=True)
    local = models.BooleanField(default=False)

    class Meta():
        verbose_name_plural = u'сервера доступа'
        verbose_name = u'сервер доступа'

    def __del__(self):
        if self.ssh:
            self.ssh.close()

    def get_networks_filter(self, **kwargs):
        qset = Q()
        for subnet in IPInterface.objects.filter(iface__nas=self):
            qset |= Q(ip__in=subnet.network)
        return qset

    def get_accounts_query(self, **kwargs):
        return Account.objects.filter(self.get_networks_filter(), **kwargs).prefetch_related('tariff')

    def get_static_account(self):
        account_up_link = {}
        for up in UpLinkPolice.objects.filter(nat_address__nas=self,
            nat_address__active=True,
            nat_address__enabled=True):
            if up.accounts:
                for account in up.accounts.filter(self.get_networks_filter()):
                    account_up_link[account] = up.nat_address
        return account_up_link


    def get_up_link_by_priority(self):
        priority_up_link = {}
        for up in self.uplink_set.filter(active=True, enabled=True):
            if up.priority in priority_up_link:
                priority_up_link[up.priority].append(up)
            else:
                priority_up_link[up.priority] = [up]
        return priority_up_link

    def get_up_link_table(self):
        account_up_link = self.get_static_account()
        top_up_link = sorted(self.get_up_link_by_priority().items(),reverse=True, key=operator.itemgetter(0))
        if len(top_up_link) >= 1:
            top_up_link = cycle(top_up_link[0][1])
        else:
            return {}

        for account in self.get_accounts_query(active=True, tariff__isnull=False, interface__isnull=True):
            if account not in account_up_link:
                account_up_link[account] = top_up_link.next()
        return account_up_link

    def get_ssh(self):
        import paramiko
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(str(self.mng_ip),
                             username=str(self.username),
                             password=str(self.password),
                             look_for_keys=False,
                             timeout=10)
        except Exception as error:
            print error
            self.ssh_error = error
            self.ssh = None
        return self.ssh

    def check_ssh(self):
        if not self.local:
            if not self.ssh and not self.ssh_error:
                self.get_ssh()
            return True
        return False

    def open(self, file_path, mode):
        if self.check_ssh():
            if not self.ssh_error:
                return self.ssh.open_sftp().open(file_path,mode)
        else:
            return open(file_path,mode)

    def listdir(self,path):
        if self.check_ssh():
            if not self.ssh_error:
                return self.ssh.open_sftp().listdir(path)
        else:
            return os.listdir(path)

    def exec_command(self, command):
        if self.check_ssh():
            if not self.ssh_error:
                return self.ssh.exec_command(command)
        else:
            return os.popen3(command)


    def __unicode__(self):
        return u'%s(%s)' % (self.name,self.mng_ip)


class NetworkInterface(models.Model):
    nas = models.ForeignKey(NasServer,verbose_name=u'Сервер доступа')
    name = models.CharField(u'Имя интервейса',max_length=30)

    class Meta():
        verbose_name_plural = u'Сетевые интерфейсы'
        verbose_name = u'Сетевой интерфейс'

    def __unicode__(self):
        return u'%s in %s' % (self.name,self.nas.__unicode__())


class IPInterface(models.Model):
    iface = models.ForeignKey(NetworkInterface, verbose_name=u'Интерфейс')
    network = IPNetworkField(u'Сеть')

    class Meta():
        verbose_name_plural = u'IP интерефейсы'
        verbose_name = u'IP интерефейс'

    def __unicode__(self):
        return u'%s in %s' % (self.network,self.iface.__unicode__())


class DHCPServer(models.Model):
    nas = models.ForeignKey(NasServer,verbose_name=u'Сервер Доступа')
    dns_first = models.IPAddressField(u'Первичный DNS')
    dns_second = models.IPAddressField(u'Вторичный DNS')

    class Meta():
        verbose_name_plural = u'Службы DHCP'
        verbose_name = u'Служба DHCP'

    def __unicode__(self):
        return u'DHCP на %s' % (self.nas.__unicode__())


class DHCPSubnet(models.Model):
    dhcp_server = models.ForeignKey(DHCPServer,verbose_name=u'Служба DHCP')
    subnet = models.ForeignKey(IPInterface,verbose_name=u'Подсеть')
    default_router  = models.IPAddressField(u'Основной маршрут')

    class Meta():
        verbose_name_plural = u'Подсети DHCP'
        verbose_name = u'Подсеть DHCP'

    def __unicode__(self):
        return self.subnet.__unicode__()


PRIORITY_CHOICES = (
    (1, u'Низкий'),
    (2, u'Ниже среднего'),
    (3, u'Средний'),
    (4, u'Выше среднего'),
    (5, u'Высокий'),
)


class UpLink(models.Model):
    nas = models.ForeignKey(NasServer, verbose_name=u'Сервер доступа')
    local_address = models.IPAddressField(u'Локальный адрес')
    remote_address = models.IPAddressField(u'Адрес шлюза')
    ipfw_nat_id = models.IntegerField(u'Номер правила трансляции в IPFW')
    priority = models.IntegerField(u'Приоритет', choices=PRIORITY_CHOICES, default=3)
    speed = models.IntegerField(u'Скорость канала в Мб', null=True, blank=True)
    enabled = models.BooleanField(u'Включина', default=False)
    active = models.BooleanField(u'Активна', default=False)

    class Meta():
        verbose_name_plural = u'Внешние каналы'
        verbose_name = u'Внешний канал'
        unique_together = ("nas", "ipfw_nat_id")
        ordering = ['nas','priority','ipfw_nat_id']

    def __unicode__(self):
        return u'%s - %s на %s' % (self.local_address,self.remote_address,self.nas.__unicode__())

class UpLinkPolice(models.Model):
    nat_address = models.ForeignKey(UpLink,verbose_name=u'Трансляция адерсов')
    network = IPNetworkField(u'Подсеть',null=True,default='0.0.0.0/32')
    accounts = models.ManyToManyField(Account,blank=True,null=True)
    priority = models.IntegerField(u'Приоритет',choices=PRIORITY_CHOICES,default=3)
    
    class Meta():
        verbose_name_plural = u'Политики внешних каналов'
        verbose_name = u'Политика внешних каналов'
        ordering = ['nat_address','priority']

    def __unicode__(self):
        return u'%s приоритет %s' % (self.nat_address.__unicode__(), self.priority)


class NetFlowProcessor(models.Model):
    nas = models.ForeignKey(NasServer, verbose_name="сервер")
    flow_source_path = models.CharField('Путь к папке с данными',
                                        max_length=100,
                                        default='/usr/local/flowdata/%Y/%Y-%m/%Y-%m-%d')
    flow_source_time_mask = models.CharField('Шаблон времени',
                                             max_length=100,
                                             default='ft-v05.%Y-%m-%d.%H%M%S')
    flow_tools_path = models.CharField('Префикc программ flowtools',
                                       max_length=100,
                                       default='/usr/local/bin')

    def __unicode__(self):
        return u'Нетфлоу на %s' % (self.nas.__unicode__())

    class Meta():
        verbose_name_plural = u'обработчики нетвлоу'
        verbose_name = u'обработчик нетфлоу'


class NetFlowSource(models.Model):
    nas = models.ForeignKey(NasServer, verbose_name='сервер')
    file_time = models.DateTimeField('время файла')
    file_name = models.CharField(max_length=100, verbose_name='имя файла')
    file_dir = models.CharField(max_length=200, verbose_name='путь к файлу')


    class Meta():
        verbose_name_plural = u'файлы нетвлоу'
        verbose_name = u'файл нетфлоу'


FIREWALL_CHOICES = (
    ("freebsd_ipfw", "freebsd_ipfw"),
    ("freebsd_ipfw_no_fwd", "freebsd_ipfw_no_fwd"),
    ("mikrotik", "mikrotik"),
    ("mikrotik_ssh", "mikrotik_ssh"),
    ("linux_ipt_tc", "linux_ipt_tc"))


class Firewall(models.Model):
    nas = models.ForeignKey(NasServer, verbose_name=u'Сервер доступа')
    kind = models.CharField(max_length="20", default="freebsd_ipfw", choices=FIREWALL_CHOICES)

    def __unicode__(self):
        return u'Фаэрвол %s на %s' % ( self.kind, self.nas.__unicode__())

    class Meta():
        verbose_name_plural = u'фаэрволы'
        verbose_name = u'фаэрвол'


class BlackListByIP(models.Model):
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    ip = IPNetworkField(verbose_name='IP Адрес')
    description = models.TextField(verbose_name='Описание')

