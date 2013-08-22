# -*- coding: utf-8 -*-Error
from probill.moon.models import MenuItems


MenuItems.add('abon',None,title='Абоненты',view_perm='billing.change_subscriber')

MenuItems.add('Пользователи',
    'loadAndRunIntoMain.billing:subscriber_index',
    parent='abon',
    view_perm='billing.change_subscriber')

MenuItems.add('Учётные записи',
    'loadAndRunIntoMain.billing:account_index',
    parent='abon',
    view_perm='billing.change_account')

MenuItems.add('История баланса',
    'loadAndRunIntoMain.billing:accounthistory_index',
    parent='abon',
    view_perm='billing.change_accounthistory')

MenuItems.add('Удобный пользователь',
    'loadAndRunIntoMain.billing:subscriber_flex',
    parent='abon',
    view_perm='billing.change_subscriber')

MenuItems.add('tariff', None, title='Тарифы', view_perm='billing.change_tariff')

MenuItems.add('Тарифы',
    'loadAndRunIntoMain.billing:tariff_index',
    parent='tariff',
    view_perm='billing.change_tariff')

MenuItems.add('История смены тарифов',
    'loadAndRunIntoMain.billing:tariffhistory_index',
    parent='tariff',
    view_perm='billing.change_tariffhistory')


MenuItems.add('Подсети',
    'loadAndRunIntoMain.billing:subnets_index',
    parent='tariff',
    view_perm='billing.change_subnets')

MenuItems.add('Шейперы и стоимость',
    'loadAndRunIntoMain.billing:qosandcost_index',
    parent='tariff',
    view_perm='billing.change_qosandcost')


MenuItems.add('admin',None,title='Админимтрирование', view_perm='billing.change_subscriber')

MenuItems.add('Менеджеры',
    'loadAndRunIntoMain.billing:manager_index',
    parent='admin',
    view_perm='billing.change_manager')

MenuItems.add('Логи сервера',
    'loadAndRunIntoMain.billing:periodiclog_index',
    parent='admin',
    view_perm='billing.change_periodiclog')


MenuItems.add('stat',None,title='Трафик', view_perm='billing.change_trafficbyperiod')

MenuItems.add('Усреднённая статистика',
    'loadAndRunIntoMain.billing:trafficbyperiod_index',
    parent='stat',
    view_perm='billing.change_trafficbyperiod')

MenuItems.add('Подробная статистика',
    'loadAndRunIntoMain.billing:trafficdetail_index',
    parent='stat',
    view_perm='billing.change_trafficdetail')