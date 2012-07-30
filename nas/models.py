# -*- coding: utf-8 -*-

from django.db import models
from probill.lib.networks import IPAddressField,IPNetworkField
from probill.billing.models import Account


class NasServer(models.Model):
    name = models.CharField(max_length=50)
    mng_ip = IPAddressField()
    secret = models.CharField(max_length=50,null=True,blank=True)

    class Meta():
        verbose_name_plural = u'Сервера доступа'
        verbose_name = u'Сервер доступа'

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
    iface = models.ForeignKey(NetworkInterface,verbose_name=u'Интерфейс')
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

PRIORITY_CHOICES = (
    (1, u'Низкий'),
    (2, u'Ниже среднего'),
    (3, u'Средний'),
    (4, u'Выше среднего'),
    (5, u'Высокий'),
)

class UpLink(models.Model):
    nas = models.ForeignKey(NasServer,verbose_name=u'Сервер доступа')
    local_address = models.IPAddressField(u'Локальный адрес')
    remote_address = models.IPAddressField(u'Адрес шлюза')
    ipfw_nat_id = models.IntegerField(u'Номер правила трансляции в IPFW')
    priority = models.IntegerField(u'Приоритет',choices=PRIORITY_CHOICES,default=3)
    enabled = models.BooleanField(u'Включина',default=False)
    active = models.BooleanField(u'Активна',default=False)

    class Meta():
        verbose_name_plural = u'Внешние каналы'
        verbose_name = u'Внешний канал'
        unique_together = ("nas", "ipfw_nat_id")
        ordering = ['priority','ipfw_nat_id']

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
        ordering = ['priority']

    