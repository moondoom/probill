from django.core.management.base import BaseCommand, CommandError
from userside.models import TblBase, TblIp, TblGroup
from billing.models import Subscriber, Tariff

class Command(BaseCommand):
    args = ''
    help = 'Handler for sync Probill and Userside'
    tariff_params = (
        ('abon','rental'),
        ('speedtx','qos_speed'),
        ('speedrx','qos_speed'),
    )
    user_params = (
        ('logname','login'),
        ('logpass','password'),
        ('fio','password'),
    )

    def compare_object(self,obj_a,obj_b,attr_list):
        result = True
        for attr in attr_list:
            if getattr(obj_a,attr[0]) <> getattr(obj_b,attr[1]):
                setattr(obj_a,attr[0],getattr(obj_b,attr[1]))
                result = False
        return result


    def sync_users(self):
        billing_users = {}
        for user in Subscriber.objects.all():
            billing_users[user.login] = user
        for user in TblBase.objects.using('userside').all():
            if user.logname in billing_users:
                self.compare_users(billing_users[user],user)
            else:
                del billing_users[user.logname]
        for user in billing_users:
            self.create_user(user)

    def sync_tariff(self):
        billing_tariff = {}
        for tar in Tariff.objects.all():
            billing_tariff[tar.name] = tar
        for tar in TblGroup.objects.using('userside').all():
            if tar.groupname in billing_tariff:
                self.check_tariff(billing_tariff[tar.groupname],tar)
                del billing_tariff[tar.groupname]
        for tar in billing_tariff:
            self.create_tariff(billing_tariff[tar])

    def create_user(self,user):
        accounts = user.account_set.all()

    def get_us_tariff(self,tariff):
        return TblGroup(
            code='probill_{}'.format(tariff.pk),
            groupname=tariff.name,
            abon=tariff.rental,
            speedtx=tariff.qos_speed,
            speedrx=tariff.qos_speed,
        )

    def create_tariff(self,tariff):
        self.get_us_tariff(tariff).save(using='userside')
        return True

    def check_tariff(self,p_tariff,u_tariff):
        if not self.compare_object(u_tariff,p_tariff,self.tariff_params):
            u_tariff.save(using='userside')
        return True

    def compare_users(self,p_user,u_user):
        if not self.compare_object(p_user,u_user,self.tariff_params):
            u_tariff.save(using='userside')

    def handle(self, *args, **options):
        self.sync_tariff()
        #self.sync_users()



