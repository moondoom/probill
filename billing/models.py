# -*- coding: utf-8 -*-

from django.db import models, connection, transaction
from django.db.models import Q
from django.contrib.admin.models import User
from django.db.utils import DatabaseError
from probill.lib.networks import IPNetworkField,IPAddressField,MACAddressField
from datetime import datetime, timedelta, time, date
from ipaddr import IPAddress
import calendar

from settings import TRUST_DAYS_COUNT

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
        return u' '.join(map(unicode,[self.datetime,self.message[:30]]))


class Manager(models.Model):
    """
    Системный пользователь способный управлять (Менеджер)
    """
    system_user = models.ForeignKey(User,unique=True,verbose_name='Системный пользователь')
    first_name = models.CharField('Фамилия',max_length=100,default='')
    last_name = models.CharField('Имя',max_length=100,default='')
    father_name = models.CharField('Отчество',max_length=100,default='')
    phone = models.CharField('Телефон',max_length=20,blank=True,null=True)

    class Meta:
        verbose_name_plural = u'менеджеры'
        verbose_name = u'менеджера'

    def __unicode__(self):
        return self.first_name

class Region(models.Model):
    name = models.CharField('Регион', max_length=100)

    class Meta:
        verbose_name_plural = u'регионы'
        verbose_name = u'регион'

    def __unicode__(self):
        return self.name



class Subscriber(models.Model):
    """
    Пользователь (подписьчик), носитель основного договора
    """
    ADDRESS_CHOICES = (
        (u'fl',u'квартира'),
        (u'of',u'офис'),
        (u'hs',u'дом')
    )
    login = models.CharField('Логин',max_length=30,unique=True,db_index=True)
    password = models.CharField('Пароль',max_length=30,blank=True,null=True)
    need_change_password = models.BooleanField("Сменить пароль", default=True)
    first_name = models.CharField('Фамилия',max_length=100)
    last_name = models.CharField('Имя',max_length=100)
    father_name = models.CharField('Отчество',max_length=100,blank=True,null=True)
    document = models.CharField('Документ',max_length=100,blank=True,null=True)
    create_date = models.DateTimeField('Дата создания',auto_now=True)
    owner = models.ForeignKey(Manager,verbose_name='Создатель')
    region = models.ForeignKey(Region,verbose_name='Регион',null=True,on_delete=models.SET_NULL)
    address_street = models.CharField('Улица',max_length=100)
    address_house = models.CharField('Дом',max_length=10)
    address_type = models.CharField('Тип адреса',max_length=2,choices=ADDRESS_CHOICES,default='fl')
    address_flat = models.CharField('Квартира',max_length=10,blank=True,null=True)
    email = models.EmailField('E-mail',blank=True,null=True)
    phone = models.CharField('Телефон',max_length=100,blank=True,null=True)
    balance = models.FloatField('Балланс',default=0)
    deleted = models.BooleanField('Удалена', default=False, editable=False)

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ['first_name','last_name','father_name']

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


    def can_trust(self):
        if self.trustpay_set.filter(end_date__gte=datetime.now()):
            return False, 'Доверительный платёж уже активирован'
        elif self.balance > 0:
            return False, 'Услуга доступна только при отрицательном балансе'
        elif self.get_rental_sum() + self.balance < 0:
            return False, 'Ваша задолженность превышает минимальную сумму абонентской платы по вашему тарифу. Доверительный платеж не может быть активирован.'
        now = date.today()
        end_day = now + timedelta(days=TRUST_DAYS_COUNT)
        first_day = now.replace(day=1)
        if self.trustpay_set.filter(create_date__gte=first_day):
            return False, 'В этом месяце вы уже воспользовались доверительным платежом.'
        if now.month != end_day.month:
            return False, 'До конца месяце осталось слишком мало дней'
        accounts = self.account_set.filter(active=False, auto_block=True).order_by('block_date')
        if accounts:
            if accounts[0].block_date.month ==  now.month:
                return True, 'Всё ок!'
            else:
                return False, 'Вы были заблокированны до начала месяца'

    def get_rental_sum(self):
        account = self.account_set.filter(active=False).aggregate(models.Sum('tariff__rental'))
        return account['tariff__rental__sum']

    def get_trust(self):
        rent_sum = self.get_rental_sum()
        TrustPay(
            subscriber=self,
            value=rent_sum,
        ).save()

    def save(self, process=True, set_delete_flag=False, *args, **kwargs):
        """
            При сохраннении обязательно проводить блокировку или разблокировку
        """
        if self.deleted:
            return None
        if set_delete_flag:
            self.deleted = True
        if not process:
            return super(Subscriber,self).save(*args,**kwargs)
        self.balance = round(self.balance,2)
        if self.balance < 0:
            for account in self.account_set.filter(active=True,auto_block=True):
                account.block()
        else:
            for account in self.account_set.filter(active=False,auto_block=True):
                account.unblock()
        super(Subscriber,self).save(*args,**kwargs)

    def delete(self, force_delete=False, *args, **kwargs):
        if force_delete:
            for account in self.account_set.all():
                account.delete(force_delete=True)
            super(Subscriber,self).delete(*args,**kwargs)
        else:
            self.save(set_delete_flag=True)

class AccountHistory(models.Model):
    """
    Финансовые операции
    """
    OWNER_CHOICES = (
        (u'man',u'Менеджер'),
        (u'per',u'Абонентская плата'),
        (u'tra',u'За тарфик'),
        (u'us',u'Из UserSide'),
        (u'syn',u'Перенесено'),
        (u'osm',u'Мультикасcа OSMP'),
        (u'tru',u'Доверительный платёж')
    )
    datetime = models.DateTimeField('Время',db_index=True)
    subscriber = models.ForeignKey(Subscriber,verbose_name='Пользователь',db_index=True)
    value = models.FloatField('Сумма')
    owner_type = models.CharField('Тип агента',max_length=3,choices=OWNER_CHOICES,default='man')
    owner_id = models.IntegerField('Агент')

    class Meta:
        verbose_name_plural = u'изменения баланса'
        verbose_name = u'измененее баланса'

    def __unicode__(self):
        return u' '.join(
            [unicode(self.datetime),
             unicode(self.subscriber),
             unicode(self.value)]
        )

    def save(self, process=True, *args, **kwargs):
        if not self.pk and process:
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
        verbose_name_plural = u'подсети'
        verbose_name_plural = u'подсеть'

    def __unicode__(self):
        return ' '.join([unicode(self.network), self.description])


class QosAndCost(models.Model):
    """
    Классы тарфика по цене и скорости
    """
    name = models.CharField('Описание',max_length=40)
    subnets = models.ManyToManyField(Subnets,verbose_name='Подсети')
    traffic_cost = models.FloatField('Стоимость МБайта',default=0)
    qos_speed = models.IntegerField('Скорость',default=0)

    class Meta:
        verbose_name_plural = u'классы трафика'
        verbose_name = u'класс трафика'
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

TIME_CHOICES = []
for hour in range(0,24):
    t = time(hour,0)
    TIME_CHOICES.append([t,t.strftime('%H:%M')])

class Tariff(models.Model):
    """
    Тарифные планы
    """
    RENTAL_CHOICES = (
        ('d','День'),
        ('m','Месяц'),
        ('w','Неделя')
    )
    name = models.CharField('Название',max_length=50,unique=True)
    rental_period = models.CharField('Период списания',max_length=1,choices=RENTAL_CHOICES,default='m')
    rental = models.FloatField('Абонетская плата',default=0)
    traffic_cost = models.FloatField('Стоимость за Мб',default=0)
    qos_speed = models.IntegerField('Основная скорость',default=0)
    qac_class = models.ManyToManyField(QosAndCost,blank=True,null=True,verbose_name='Классы трафика')
    speed_up = models.IntegerField('Коэффициент ускорения',default=1)
    speed_up_start = models.TimeField('Время включения ускорения',default=time(22,0),choices=TIME_CHOICES)
    speed_up_end = models.TimeField('Время выключения ускорения',default=time(6,0),choices=TIME_CHOICES)
    archive = models.BooleanField('Архивный тариф', default=False)


    class Meta:
        verbose_name_plural = u'Тарифные планы'

    def __unicode__(self):
        return self.name

    @property
    def bit_speed(self):
        return self.get_speed() * 1024

    def get_speed(self):
        if self.speed_up > 1:
            now = datetime.now().time()
            if self.speed_up_start > self.speed_up_end:
                if now >= self.speed_up_start or (0 <= now < self.speed_up_end):
                    return self.qos_speed * self.speed_up
            else:
                if self.speed_up_start <= now < self.speed_up_end:
                    return self.qos_speed * self.speed_up
        return self.qos_speed

    def get_account_count(self):
        return self.account_set.count()

    get_account_count.short_description = 'Колво Абонентов'

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
            return self.rental - self.rental / 7 * date.weekday
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

STATE_CHOICES = (
    (200, u'Работает'),
    (301, u'Новый'),
    (302, u'Импортирован'),
    (401, u'Приостановлен'),
    (402, u'Долг'),
    (404, u'Отключен'),
    (500, u'Авария'),
    )

class AccountLog(models.Model):
    datetime = models.DateTimeField("Дата/Время", auto_created=True)
    account = models.ForeignKey("Account", verbose_name="Учётная запись")
    old_status = models.IntegerField("Был", choices=STATE_CHOICES)
    new_status = models.IntegerField("Стал", choices=STATE_CHOICES)

class Account(models.Model):
    """
    Учётные записи пользователей
    """


    subscriber = models.ForeignKey(Subscriber,verbose_name='Пользователь')
    login = models.CharField('Имя учётной записи',max_length=30,unique=True,db_index=True)
    password = models.CharField('Пароль',max_length=30,blank=True,null=True)
    tariff = models.ForeignKey(Tariff,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='Тариф')
    ip = IPAddressField('IP адрес',db_index=True, null=True, blank=True)
    mac = MACAddressField('MAC адрес',max_length=17, blank=True, null=True)
    create_date = models.DateTimeField('Дата создания', auto_now=True)
    owner = models.ForeignKey(Manager,verbose_name='Создатель',db_index=True)
    block_date = models.DateTimeField('Дата блокировки',null=True,editable=False)
    auto_block = models.BooleanField('Автоматическая блокировка',default=True)
    active = models.BooleanField('Активна',default=True)
    status = models.IntegerField('Статус', default=200, choices=STATE_CHOICES)
    deleted = models.BooleanField('Удалена', default=False, editable=False)
    #alt_route = models.BooleanField('Альтернативный маршрут',default=False)

    class Meta:
        verbose_name_plural = u'Учётные записи'

    def __unicode__(self):
        return self.login

    def save(self, process=True, set_delete_flag=False, *args,  **kwargs):
        if self.deleted:
            return None
        if set_delete_flag:
            self.deleted = True

        if not process:
            return super(Account,self).save(*args,**kwargs)
        if self.pk:
            old = Account.objects.get(id = self.id)
            old_tariff = old.tariff
        else:
            old = None
            old_tariff = None
        super(Account,self).save(*args,**kwargs)
        # Проверяем не сменился ли тариф
        if old_tariff != self.tariff:
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
        # Проверяем изменение статуса
        if old:
            if self.status != old.status:
                AccountLog(account=self, old_status=old.status, new_status=self.status)

    def clean_traffic(self):
        if self.pk:
            cursor = connection.cursor()
            cursor.execute('delete from tdcore where account_id = %s', [self.pk])
            cursor.execute('delete from billing_trafficbyperiod where account_id = %s', [self.pk])


    def delete(self, force_delete=False, *args, **kwargs):
        if force_delete:
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
            self.clean_traffic()
            super(Account,self).delete(*args,**kwargs)
        else:
            self.save(set_delete_flag=True)


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
                src_ip,
                dst_ip,
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
    account = models.ForeignKey(Account,verbose_name='Учётная запись')
    tariff = models.ForeignKey(Tariff,verbose_name='Тариф')

    class Meta:
        verbose_name_plural = u'История смены тарифа'

    def __unicode__(self):
        return  ' '.join([unicode(self.set_data),unicode(self.account)])


class TrafficByPeriod(models.Model):
    """
        Количество трафика потреблённого за отчётные период
    """
    datetime = models.DateTimeField('Время',db_index=True)
    account = models.ForeignKey("Account",verbose_name='Учётная запись',db_index=True)
    tariff = models.ForeignKey("Tariff",verbose_name='Тариф')
    qac_class = models.ForeignKey("QosAndCost",blank=True,null=True,verbose_name='Класс трафика')
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
    account = models.ForeignKey("Account",blank=True,null=True,verbose_name='Учётная запись',db_index=True,editable=False)

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
            if e.args[0].count('не существует'):

                start_date = datetime.combine(date, time(0))
                end_date = start_date + timedelta(1) - timedelta(0, 0, 0, 1)
                sql = '''
                CREATE TABLE {0} (
                    CHECK (datetime BETWEEN '{1}+07'::timestamp with time zone AND '{2}+07'::timestamp with time zone)
                ) INHERITS ({3});
                CREATE INDEX "{0}_datetime" ON "{0}" ("datetime");
                CREATE INDEX "{0}_account_id" ON "{0}" ("account_id");
                '''.format(table_name, start_date, end_date, cls._meta.db_table)
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


OSMP_CHOICES = (
    (0,'check'),
    (1, 'pay'),
    (666, 'error')
)


class OsmpPay(models.Model):

    process_date = models.DateTimeField(verbose_name="Дата сообщения", auto_now_add=True)
    pay_date = models.DateTimeField(verbose_name="Дата операции", null=True)
    command = models.IntegerField(choices=OSMP_CHOICES, verbose_name="Команда")
    value = models.FloatField(verbose_name="Сумма")
    osmp_txn_id = models.BigIntegerField(verbose_name="Код операции")
    prv_txn = models.ForeignKey(AccountHistory,verbose_name="Операция", null=True)
    result = models.IntegerField(verbose_name="Код завершения")
    comment = models.TextField(verbose_name="Коментарий")
    error = models.BooleanField(verbose_name="Ошибка обработки", blank=True, default=False)

    class Meta:
        verbose_name_plural = u'Платежи OSMP'


class TrustPay(models.Model):
    subscriber = models.ForeignKey(Subscriber,verbose_name="Пользователь")
    create_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True, editable=False)
    end_date = models.DateTimeField(verbose_name="Дата окончания", blank=True, editable=False)
    trust_days = models.PositiveSmallIntegerField(verbose_name="Количество дней", default=TRUST_DAYS_COUNT)
    value = models.PositiveIntegerField(verbose_name="Сумма")
    active = models.BooleanField(verbose_name="Активна", default=True, editable=False)
    manager = models.ForeignKey(Manager, verbose_name="Менеджер", null=True, blank=True, editable=False)

    class Meta:
        verbose_name_plural = u'Доверительные платежи'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.create_date = datetime.now()
            self.end_date = self.create_date + timedelta(days=self.trust_days)
            super(TrustPay,self).save(*args,**kwargs)
            self.activate()
        elif not self.active:
            super(TrustPay,self).save(*args,**kwargs)

    def delete(self, *args, **kwargs):
        if self.pk:
            self.deactivate()
        super(TrustPay,self).delete()

    def activate(self):
        AccountHistory(datetime=datetime.now(),
                       subscriber=self.subscriber,
                       value=self.value,
                       owner_type='tru',
                       owner_id=self.pk).save()


    def deactivate(self):
        if self.active:
            AccountHistory(datetime=datetime.now(),
                           subscriber=self.subscriber,
                           value= -self.value,
                           owner_type='tru',
                           owner_id=self.pk).save()
            self.active = False
        super(TrustPay,self).save()



from south.modelsinspector import add_introspection_rules

rules = [
    (
        (IPNetworkField, IPAddressField, MACAddressField), [],
        {}
        ),
    ]

add_introspection_rules(rules, [".*(IP|MAC).*Field"])