# coding=utf-8
from django.db import models
from nas.models import NasServer
from lib.networks import IPAddressField, IPNetworkField


class AstraServer(models.Model):
    nas = models.ForeignKey(NasServer)
    http_address = IPAddressField(null=True, blank=True, verbose_name="Адресс сервера для HTTP")
    multi_cast_network = IPNetworkField(null=True, blank=True, verbose_name="Сеть для мультикаста")
    multi_cast_port = models.IntegerField(null=True, blank=True, verbose_name="Порт мультикаста")

    def __unicode__(self):
            return  "{} ({})".format(self.nas, self.http_address)


class AstraConfig(models.Model):
    name = models.CharField("Имя адаптера", max_length=100)
    astra_server = models.ForeignKey(AstraServer,verbose_name="Сервер Астры")
    file_path = models.CharField("Путь к конфигурации", max_length=200)
    config_head = models.TextField("Заголовок конфигурации")
    http_port = models.IntegerField("Порт HTTP-сервера")

    def __unicode__(self):
            return  "{} на {}".format(self.name)

class SimpleChannel(models.Model):

    def get_url(self):
        return


class AstraChannel (SimpleChannel):
    astra_config = models.ForeignKey(AstraConfig, verbose_name="Конфигурация Астры")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    astra_input = models.CharField(max_length=200)
    chanel_id = models.CharField(max_length=100)

    def __unicode__(self):
        return  "{}".format(self.description)

    def get_url(self):
        return 'http://{}:{}/{}'.format(self.astra_config.astra_server.http_address,
                                        self.astra_config.http_port,
                                        self.chanel_id)


class LocalChannel (SimpleChannel):
    url = models.CharField("Ссылка на канал", max_length=200)
    description = models.CharField("Описание", max_length=200)

    def __unicode__(self):
        return  "{}".format(self.description)

    def get_url(self):
        return self.url


class M3UPlayList(models.Model):
    nas = models.ForeignKey(NasServer)
    file_location = models.CharField("Расположение файла",max_length=200)
    astra_channel = models.ManyToManyField(AstraChannel, verbose_name="Каналы IPTV")
    local_channel = models.ManyToManyField(LocalChannel, verbose_name="Локальные каналы")

    def __unicode__(self):
        return  "{} {}".format(self.nas, self.file_location)


class SSIPTVChannel(models.Model):
    ss_id = models.IntegerField("ID канала", db_index=True)
    ss_title = models.CharField(max_length=100)
    is_local = models.BooleanField("Локальный канал", default=False)

    def __unicode__(self):
        return  "{}".format(self.ss_title)


class SSIPTVPlayList(models.Model):
    package_title = models.CharField("Заголовог плей-листа", max_length=100)
    city = models.CharField("Название города", max_length=100)
    package_id = models.IntegerField("ИД плей-листа")

    def __unicode__(self):
        return  "{} {}".format(self.package_title, self.city)


class SSIPTV2Channel(models.Model):
    astra_channel = models.ForeignKey(SimpleChannel,
                                      verbose_name="Канал IPTV",
                                      null=True,
                                      on_delete=models.SET_NULL)
    ss_iptv_channel = models.ForeignKey(SSIPTVChannel,
                                        verbose_name="Канал SS-IPTV", null=True,
                                        on_delete=models.SET_NULL)

