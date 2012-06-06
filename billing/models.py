# -*- coding: utf-8 -*-

from django.db import models, connection, transaction
from django.db.models import Q
from django.contrib.admin.models import User
from django.db.utils import DatabaseError
from probill.lib.networks import IPNetworkField,IPAddressField
from datetime import datetime, timedelta
from ipaddr import IPAddress
import calendar

class PeriodicLog(models.Model):
    datetime = models.DateTimeField()
    code = models.IntegerField(default=0)
    message = models.TextField()


    class Meta():
        verbose_name_plural = u'Переодические логи'
        verbose_name = u'Запись'

    @classmethod
    def log(cls,message,code=0):
        obj = cls(datetime=datetime.now(),message=message,code=code)
        obj.save()

    def __unicode__(self):
        return ' '.join(map(unicode,[self.datetime,self.message[:30]]))


class Manager(models.Model):
    """
    Системный пользователь способный управлять (Менеджер)
    """
    system_user = models.ForeignKey(User,unique=True,verbose_name=u'Системный пользователь')
    first_name = models.CharField(u'Фамилия',max_length=100,default='')
    last_name = models.CharField(u'Имя',max_length=100,default='')
    father_name = models.CharField(u'Отчество',max_length=100,default='')
    phone = models.CharField(u'Телефон',max_length=20,blank=True,null=True)

    class Meta:
        verbose_name_plural = u'Менеджеры'

    def __unicode__(self):
        return self.first_name

class Subscriber(models.Model):
    """
    Пользователь (подписьчик), носитель основного договора
    """
    ADDRESS_CHOICES = (
        (u'fl',u'квартира'),
        (u'of',u'офис'),
        (u'hs',u'дом')
    )
    login = models.CharField(u'Имя учётной записи',max_length=30,unique=True,db_index=True)
    password = models.CharField(u'Пароль',max_length=30,blank=True,null=True)
    first_name = models.CharField(u'Фамилия',max_length=100)
    last_name = models.CharField(u'Имя',max_length=100)
    father_name = models.CharField(u'Отчество',max_length=100,blank=True,null=True)
    document = models.CharField(u'Документ',max_length=100,blank=True,null=True)
    create_date = models.DateTimeField(u'Дата создания',auto_now=True)
    owner = models.ForeignKey(Manager,verbose_name=u'Создатель')
    address_street = models.CharField(u'Улица',max_length=100)
    address_house = models.CharField(u'Дом',max_length=10)
    address_type = models.CharField(u'Тип адреса',max_length=2,choices=ADDRESS_CHOICES,default='fl')
    address_flat = models.CharField(u'Квартира',max_length=10,blank=True,null=True)
    email = models.EmailField(u'E-mail',blank=True,null=True)
    phone = models.CharField(u'Телефон',max_length=100,blank=True,null=True)
    balance = models.FloatField(u'Балланс',default=0)


    class Meta:
        verbose_name_plural = u'Пользователи'
        verbose_name = u'Пользователь'

    def __unicode__(self):
        return u' '.join(
            [self.first_name,
            self.last_name,
            ]
        )

    @property
    def addressString(self):
        if self.address_flat:
            return ' '.join([self.address_street,
                             self.address_house ,
                             self.get_address_type_display(),
                             self.address_flat])
        else:
            return self.address_street + ' ' + self.address_house
    def save(self, *args, **kwargs):
        """
            При сохраннении обязательно проводить блокировку или разблокировку
        """
        if self.balance < 0:
            for account in self.account_set.filter(active=True,auto_block=True):
                account.block()
        else:
            for account in self.account_set.filter(active=False,auto_block=True):
                account.unblock()
        super(Subscriber,self).save(*args,**kwargs)

class AccountHistory(models.Model):
    """
    Финансовые операции
    """
    OWNER_CHOICES = (
        (u'man',u'Менеджер'),
        (u'per',u'Абонентская плата'),
        (u'tra',u'За тарфик')
    )
    datetime = models.DateTimeField(u'Время',db_index=True)
    subscriber = models.ForeignKey(Subscriber,db_index=True)
    value = models.FloatField(u'Сумма')
    owner_type = models.CharField(u'Тип агента',max_length=3,choices=OWNER_CHOICES)
    owner_id = models.IntegerField(u'Агент')


    class Meta:
        verbose_name_plural = u'Cписания и начисления'

    def __unicode__(self):
        return u' '.join(
            [unicode(self.datetime),
             unicode(self.subscriber),
             unicode(self.value)]
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.subscriber.balance += self.value
            self.subscriber.save()
            super(AccountHistory,self).save(*args,**kwargs)



class Subnets(models.Model):
    """
    Подсети для деления трафика по категориям
    """
    network = IPNetworkField('Подсеть')
    description = models.CharField('Описание',max_length=100,default='',blank=True)


    class Meta:
        verbose_name_plural = u'Подсети'

    def __unicode__(self):
        return ' '.join([unicode(self.network), self.description])


class QosAndCost(models.Model):
    """
    Классы тарфика по цене и скорости
    """
    name = models.CharField('Описание',max_length=40)
    subnets = models.ManyToManyField(Subnets,verbose_name=u'Подсети')
    traffic_cost = models.FloatField('Стоимость МБайта',default=0)
    qos_speed = models.IntegerField('Скорость',default=0)


    class Meta:
        verbose_name_plural = u'Классы трафика'
        ordering = ['-id']

    def __unicode__(self):
        return self.name

    @property
    def bit_speed(self):
        return self.qos_speed*1024

    @property
    def subnets_iter(self):
        if not hasattr(self,'_subnets'):
            self._subnets = self.subnets.all()
        return self._subnets


class Tariff(models.Model):
    """
    Тарифные планы
    """
    RENTAL_CHOICES = (
        ('d','День'),
        ('m','Месяц'),
        ('w','Неделя')
    )
    name = models.CharField(max_length=50,unique=True)
    rental_period = models.CharField(u'Период списания',max_length=1,choices=RENTAL_CHOICES,default='m')
    rental = models.FloatField(u'Абонетская плата',default=0)
    traffic_cost = models.FloatField('Стоимость за Мб',default=0)
    qos_speed = models.IntegerField('Основная скорость',default=0)
    qac_class = models.ManyToManyField(QosAndCost,blank=True,null=True,verbose_name=u'Классы трафика')

    class Meta:
        verbose_name_plural = u'Тарифные планы'

    def __unicode__(self):
        return self.name

    @property
    def bit_speed(self):
        return self.qos_speed*1024

    @property
    def qac_iter(self):
        if not hasattr(self,'_qac_class'):
            self._qac_class = self.qac_class.all()
        return self._qac_class

    def get_traffic_qac(self,src_ip):
        src_ip = IPAddress(src_ip)
        for qac in self.qac_iter:
            for net in qac.subnets_iter:
                if src_ip in net.network:
                    return qac
        return None

    def getRentalDiff(self):
        date = datetime.now()
        if not self.rental:
            return 0
        if self.rental_period == 'h':
            return self.rental
        elif self.rental_period == 'w':
            return self.rental - self.rental/7*date.weekday
        elif self.rental_period == 'm':
            days = calendar.mdays[date.month]
            return self.rental - self.rental/days*date.day
        return 0

    @classmethod
    def doPeriodRental(cls,date=None):
        account_count = 0
        rental_sum = 0
        if not date:
            date = datetime.now()
        if not date.hour:
            q_filter = Q(rental_period='h')
            if date.weekday == 1:
                q_filter.add(Q(rental_period='w'),Q.OR)
            if date.day == 1:
                q_filter.add(Q(rental_period='m'),Q.OR)
            for tariff in cls.objects.filter(q_filter).exclude(rental=0):
                for account in tariff.account_set.filter(active=True):
                    accHist = AccountHistory(
                        datetime = date,
                        owner_id = tariff.id,
                        owner_type = 'per',
                        subscriber = account.subscriber,
                        value = -tariff.rental
                    )
                    accHist.save()
                    account_count += 1
                    rental_sum += tariff.rental
            return 'Переодическое списание завершено успешно. Снять %s c %s пользователей' % \
                   (rental_sum,account_count), 100
        else:
            return 'Сейчас не 0 часов. Проверьте параметры запуска скрипта или настройки cron', 100


    @classmethod
    def calcRentalDiff(cls,from_tar,to_tar):
        if from_tar and to_tar:
            return from_tar.getRentalDiff() - to_tar.getRentalDiff()
        elif from_tar:

            return from_tar.getRentalDiff()
        elif to_tar:
            return - to_tar.getRentalDiff()
        else:
            return 0

class Account(models.Model):
    """
    Учётные записи пользователей
    """
    subscriber = models.ForeignKey(Subscriber,verbose_name=u'Пользователь')
    login = models.CharField('Имя учётной записи',max_length=30,unique=True,db_index=True)
    password = models.CharField('Пароль',max_length=30,blank=True,null=True)
    tariff = models.ForeignKey(Tariff,on_delete=models.SET_NULL,null=True,blank=True,verbose_name=u'Тариф')
    ip = IPAddressField('IP адрес',unique=True,db_index=True)
    mac = models.CharField('MAC адрес',max_length=17,blank=True,null=True)
    create_date = models.DateTimeField('Дата создания',auto_now=True)
    owner = models.ForeignKey(Manager,verbose_name=u'Создатель',db_index=True)
    block_date = models.DateTimeField('Дата блокировки',null=True,editable=False)
    auto_block = models.BooleanField('Автоматическая блокировка',default=True)
    active = models.BooleanField('Активна',default=True)

    class Meta:
        verbose_name_plural = u'Учётные записи'

    def __unicode__(self):
        return self.login

    def save(self, *args, **kwargs):
        if self.pk:
            old = Account.objects.get(id = self.id)
            old_tariff = old.tariff
        else:
            old_tariff = None
        if old_tariff <> self.tariff:
            rentalDiff = Tariff.calcRentalDiff(old_tariff,self.tariff)
            if rentalDiff:
                accHist = AccountHistory(
                    datetime=datetime.now(),
                    owner_id = self.subscriber.id,
                    owner_type = 'per',
                    subscriber = self.subscriber,
                    value = rentalDiff
                )
                accHist.save()
        super(Account,self).save(*args,**kwargs)

    def delete(self, *args, **kwargs):
        rentalDiff = Tariff.calcRentalDiff(self.tariff,None)
        if rentalDiff:
            accHist = AccountHistory(
                datetime=datetime.now(),
                owner_id = self.id,
                owner_type = 'per',
                subscriber = self.subscriber,
                value = rentalDiff
            )
            accHist.save()
        super(Account,self).delete(*args,**kwargs)

    def block(self):
        self.block_date = datetime.now()
        self.active = False
        self.save()

    def unblock(self):
        self.active = True
        self.save()


    @property
    def CIDR(self):
        return '/'.join([str(self.ip),'32'])



    @classmethod
    def process_traffic(cls,raw_traffic,traffic_datetime):

        good_ip = {}
        bad_ip = []
        traffic_periods = {}
        traffic_details = []
        for row in raw_traffic:
            src_ip = row[0]
            dst_ip = row[1]
            count = row[2]/1024/1024
            if dst_ip not in good_ip and dst_ip not in bad_ip:
                try:
                    good_ip[dst_ip] = cls.objects.get(ip=dst_ip)
                except :
                    bad_ip.append(dst_ip)
            traffic_details.append(
                [traffic_datetime,
                dst_ip,
                src_ip,
                count,
                None]
            )
            if dst_ip in good_ip:
                traffic_details[-1][-1] = good_ip[dst_ip].id
                qac = good_ip[dst_ip].tariff.get_traffic_qac(src_ip)
                if qac:
                    period_id = '_'.join([dst_ip, str(qac.id)])
                else:
                    period_id = dst_ip
                if period_id in traffic_periods:
                    traffic_periods[period_id].count += count
                else:
                    traffic_periods[period_id] = TrafficByPeriod(
                        account = good_ip[dst_ip],
                        cost = 0,
                        count = count,
                        datetime = traffic_datetime,
                        qac_class = qac,
                        tariff = good_ip[dst_ip].tariff
                    )
        TrafficDetail.insert_many(traffic_details)
        for i in traffic_periods:
            if traffic_periods[i].qac_class:
                traffic_periods[i].cost = traffic_periods[i].count * traffic_periods[i].qac_class.traffic_cost
            else:
                traffic_periods[i].cost = traffic_periods[i].count * traffic_periods[i].account.tariff.traffic_cost
            traffic_periods[i].save()
            if traffic_periods[i].cost > 0:
                accHist = AccountHistory(
                    datetime=traffic_datetime,
                    owner_id = traffic_periods[i].id,
                    owner_type = 'tra',
                    subscriber = traffic_periods[i].account.subscriber,
                    value = -traffic_periods[i].cost
                )
                accHist.save()
        PeriodicLog.log('Обработка трафика. Снято %s с %s учётных записей' % (1,1))


class TariffHistory(models.Model):
    """
        История смены тарифов
    """
    set_data = models.DateTimeField('Время установки',auto_now=True)
    account = models.ForeignKey(Account,verbose_name=u'Учётная запись')
    tariff = models.ForeignKey(Tariff,verbose_name=u'Тариф')

    class Meta:
        verbose_name_plural = u'История смены тарифа'

    def __unicode__(self):
        return  ' '.join([unicode(self.set_data),unicode(self.account)])


class TrafficByPeriod(models.Model):
    """
        Количество трафика потреблённого за отчётные период
    """
    datetime = models.DateTimeField('Время',db_index=True)
    account = models.ForeignKey("Account",verbose_name=u'Учётная запись',db_index=True)
    tariff = models.ForeignKey("Tariff",verbose_name=u'Тариф')
    qac_class = models.ForeignKey("QosAndCost",blank=True,null=True,verbose_name=u'Класс трафика')
    count = models.FloatField('Количество')
    cost = models.FloatField('Стоимость по тарифу')

    class Meta:
        verbose_name_plural = u'Количественная статистика'

    def __unicode__(self):
        return  ' '.join([unicode(self.datetime),unicode(self.account),unicode(self.count)])

class TrafficDetail(models.Model):
    """
        Детальная статистика за период
    """
    datetime = models.DateTimeField('Время',db_index=True,editable=False)
    src_ip = IPAddressField('Источник',editable=False)
    dst_ip = IPAddressField('Назначение',editable=False)
    count = models.FloatField('Количество',editable=False)
    account = models.ForeignKey("Account",blank=True,null=True,verbose_name=u'Учётная запись',db_index=True,editable=False)

    class Meta:
        verbose_name_plural = u'Подробная статистика'
        db_table = 'tdcore'


    @classmethod
    def check_table_name(cls,date):
        table_name =  cls._meta.db_table + date.strftime('%Y%m%d')
        cursor = connection.cursor()
        try:
            cursor.execute('select * from %s limit 1' % table_name)
        except DatabaseError, e:
            transaction.commit_unless_managed()
            if e.args[0].count('does not exist'):
                start_date = date.strftime('%Y-%m-%d')
                end_date = (date + timedelta(1)).strftime('%Y-%m-%d')
                sql = '''
                CREATE TABLE %s (
                    CHECK ( datetime >= DATE '%s' AND datetime < DATE '%s' )
                ) INHERITS (%s);
                ''' % (table_name,start_date,end_date,cls._meta.db_table)
                cursor.execute(sql)
        return table_name

    @classmethod
    def insert_many(cls,traffic_details):
        traffic_by_date = {}
        for traffic in traffic_details:
            date = traffic[0].date()
            if date in traffic_by_date:
                traffic_by_date[date].append(traffic)
            else:
                traffic_by_date[date] = [traffic]
        cursor = connection.cursor()
        for date in traffic_by_date:
            query = '''
                insert into %s (datetime,src_ip,dst_ip,"count",account_id)
                values (%%s,%%s,%%s,%%s,%%s)
                ''' % cls.check_table_name(date)
            cursor.executemany(query,traffic_details)
        cursor.connection.commit()

    def __unicode__(self):
        return  ' '.join([unicode(self.datetime),unicode(self.src_ip),unicode(self.dst_ip)])




