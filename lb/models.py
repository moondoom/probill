# coding=utf-8

from django.db import models
from billing.models import Subscriber
# Create your models here.


class ExportedSub(models.Model):

    subscriber = models.ForeignKey(Subscriber,verbose_name="Пользователь")
    lb_id = models.IntegerField("ИД в базе ландилинга")
    create_date = models.DateTimeField("Время экспортирования", auto_now_add=True)