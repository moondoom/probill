
from probill.moon.lib.jqgrid import JqGridView , JqTreeGridView
from models import *


class SubscriberGrid(JqGridView):
    app_name = 'billing'
    model = Subscriber

subscriber_grid = SubscriberGrid()

class AccountGrid(JqGridView):
    app_name = 'billing'
    model = Account

account_grid = AccountGrid()

class AccountHistoryGrid(JqGridView):
    app_name = 'billing'
    model = AccountHistory
    aed = {
        'add':True,
        'delete':False,
        'edit':False,
    }

accounthistory_grid = AccountHistoryGrid()

class TariffGrid(JqGridView):
    app_name = 'billing'
    model = Tariff

tariff_grid = TariffGrid()

class TariffHistoryGrid(JqGridView):
    app_name = 'billing'
    model = TariffHistory

tariffhistory_grid = TariffHistoryGrid()

class SubnetsGrid(JqGridView):
    app_name = 'billing'
    model = Subnets

subnets_grid = SubnetsGrid()

class QosAndCostGrid(JqGridView):
    app_name = 'billing'
    model = QosAndCost

qosandcost_grid = QosAndCostGrid()

class ManagerGrid(JqGridView):
    app_name = 'billing'
    model = Manager

manager_grid = ManagerGrid()

class PeriodicLogGrid(JqGridView):
    app_name = 'billing'
    model = PeriodicLog

periodiclog_grid = PeriodicLogGrid()

class TrafficByPeriodGrid(JqGridView):
    app_name = 'billing'
    model = TrafficByPeriod

trafficbyperiod_grid = TrafficByPeriodGrid()

class TrafficDetailGrid(JqGridView):
    app_name = 'billing'
    model = TrafficDetail


trafficdetail_grid = TrafficDetailGrid()






