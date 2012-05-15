# -*- coding: utf-8 -*-

from django.db import models
from probill.lib.networks import IPAddressField,IPNetworkField


class NasServer(models.Model):
    name = models.CharField(max_length=50)
    mng_ip = IPAddressField()
    secret = models.CharField(max_length=50,null=True,blank=True)

    class Meta():
        verbose_name_plural = u'Сервера доступа'
        verbose_name = u'Сервер доступа'

class NetworkInterface(models.Model):
    nas = models.ForeignKey(NasServer,verbose_name=u'Сервер доступа')
    name = models.CharField(u'Имя интервейса',max_length=30)

    class Meta():
        verbose_name_plural = u'Сетевые интерфейсы'
        verbose_name = u'Сетевой интерфейс'

class IPInterface(models.Model):
    iface = models.ForeignKey(NetworkInterface,verbose_name=u'Интерфейс')
    network = IPNetworkField(u'Сеть')

    class Meta():
        verbose_name_plural = u'IP интерефейсы'
        verbose_name = u'IP интерефейс'


class DHCPServer(models.Model):
    nas = models.ForeignKey(NasServer,verbose_name=u'Сервер Доступа')
    dns_first = models.IPAddressField(u'Первичный DNS')
    dns_second = models.IPAddressField(u'Вторичный DNS')

    class Meta():
        verbose_name_plural = u'Службы DHCP'
        verbose_name = u'Служба DHCP'

class DHCPSubnet(models.Model):
    dhcp_server = models.ForeignKey(DHCPServer,verbose_name=u'Служба DHCP')
    subnet = models.ForeignKey(IPInterface,verbose_name=u'Подсеть')
    default_router  = models.IPAddressField(u'Основной маршрут')

    class Meta():
        verbose_name_plural = u'Подсети DHCP'
        verbose_name = u'Подсеть DHCP'


