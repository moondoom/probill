# -*- coding: utf-8 -*-
import mptt
from mptt.models import TreeForeignKey, MPTTModel
from django.db import models
from settings import DEBUG
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class MenuItems(MPTTModel):
    name = models.CharField('Имя',max_length=30,unique=True)
    title = models.CharField('Заголовок',max_length=50)
    action = models.CharField('Действие',max_length=100,blank=True,null=True)
    order = models.IntegerField('Очередь',default=1,blank=True)
    parent = TreeForeignKey('self',verbose_name='Родитель',null=True,blank=True,related_name='children')
    view_perm = models.CharField('Привелении',max_length=100)
    auto_created = models.BooleanField(default=True,blank=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['order','name']

    class Meta:
        permissions = (('view_menu', 'Может просматривать menu'),)

    def __unicode__(self):
        return self.title

    def get_action(self):
        if self.action:
            try:
                res = self.action.split('.')
                obj, action = res[0], reverse(res[1])
                return '%s("%s")' % (obj,action)
            except :
                pass
        return ''

    @classmethod
    def add(cls,name,action,order=1,parent=None,title=None,view_perm='pnk.view_menu'):
        if not title:
            title = name
        if parent:
            parent, created = cls.objects.get_or_create(name=parent)
            if parent.action:
                parent.action = None
                parent.save()
        menu, created =  cls.objects.get_or_create(
            name = name,
            defaults={
                'title': title,
                'action':action,
                'order': order,
                'parent': parent,
                'view_perm': view_perm
            }
        )
        if not created:
            if DEBUG:
                print 'Override menu item %s' % menu
            menu.action = action
            menu.order = order
            menu.parent = parent
            menu.view_perm = view_perm
            menu.save()

