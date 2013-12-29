# -*- coding: utf-8 -*-
import string

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from billing.models import *
import settings

import datetime
import json
from math import ceil
import re

def parse_date(request):
    try:
        sdate = datetime.datetime.strptime(request.GET['sdate'],'%Y-%m-%d').date()
    except:
        sdate = datetime.date.today()
    try:
        edate = datetime.datetime.strptime(request.GET['edate'],'%Y-%m-%d').date()
    except:
        edate = None
    if not edate or edate == sdate:
        edate = sdate + datetime.timedelta(days=1)
    elif sdate > edate:
        tmdate = edate
        edate = sdate
        sdate = tmdate
    return sdate , edate


def sub_auth(fn):
    """
       Подменяет стандартного пользователя user на subscriber
       """
    def new (request,*arg,**kwargs):
        if 'subscriber_id' in request.session:
            try:
                request.user = Subscriber.objects.get(id=request.session['subscriber_id'])
            except ObjectDoesNotExist:
                return logout(request)
            return fn(request,*arg,**kwargs)
        else:
            return login(request)
    return new

@sub_auth
def index(request,template='client_main.html'):
    c = RequestContext(request)
    return render_to_response(template, c)

@sub_auth
def trust_pay(request):
    c = RequestContext(request)
    sub = c['user']
    ok, message = sub.can_trust()
    if ok and request.GET.has_key('get_trust'):
        sub.get_trust()
        message = 'Поздравляем! Доверительный платеж успешно ативирован.'
        ok = False
    elif ok:
        message = ''

    c['message'] = message
    c['ok'] = ok
    return render_to_response('client_trust_pay.html',c)

@sub_auth
def change_password(request):
    c = RequestContext(request)
    sub = c['user']
    if sub.need_change_password:
        if request.POST.has_key('password') and request.POST.has_key('re_password'):
            password = unicode(request.POST['password'])
            re_password = unicode(request.POST['re_password'])
            c['password'], c['re_password'] = password, re_password
            if len(password) < 6:
                c['message'] = 'Длинна пароля меньше 6 символов'
            elif password != re_password:
                c['message'] = 'Пароли не совпадают'
            elif password == sub.password:
                c['message'] = 'Пароль совпадает со старым'
            elif [f for f in password if f not in string.printable]:
                c['message'] = 'Пароль содержит недопустимые символы'
            else:
                sub.password = password
                sub.need_change_password = False
                sub.save()
                return HttpResponseRedirect('/client')
        else:
            c['message'] = "Вам необходимо сменить пароль"
        return  render_to_response("client_change_password.html", c)
    elif request.GET.has_key('user_request'):
        sub.need_change_password = True
        sub.save()
        return  render_to_response("client_change_password.html", c)
    else:
        return HttpResponseRedirect('/client')


def only_ip_auth(request,template='client_blocked.html'):
    c = RequestContext(request)
    c['REMOTE_ADDR'] = request.META['REMOTE_ADDR']
    return render_to_response(template, c)

@sub_auth
def stat_json(request):
    start_date , end_date = parse_date(request)
    try:
        limit = int(request.GET['rows'])
        page = int(request.GET['page'])
    except KeyError:
        return Http404()
    try:
        sidx = request.GET['sidx']
        sord = request.GET['sord']
    except KeyError:
        sidx = 'datetime'
        sord = 'desc'
    if not end_date or end_date == start_date:
        end_date = start_date + datetime.timedelta(days=1)
    elif start_date > end_date:
        tmp_date = end_date
        end_date = start_date
        start_date = tmp_date
        del tmp_date
    traffic_stat = TrafficDetail.objects.filter(datetime__gte=start_date,
        datetime__lte=end_date,
        account__subscriber=request.user)
    if sord == 'asc':
        traffic_stat = traffic_stat.order_by(sidx)
    else:
        traffic_stat = traffic_stat.order_by("-" + sidx)
    if len(traffic_stat) > 0:
        total_pages = int(ceil(float(len(traffic_stat))/limit))
    else:
        total_pages = 0
    if page > total_pages:
        page = total_pages
    start = limit * page - limit
    if start < 0:
        start = 0
    end = start + limit
    response = {'page': page, 'total': total_pages, 'records': len(traffic_stat), 'rows': []}
    for rows in traffic_stat.values()[start:end]:
        rows['datetime'] = str(rows['datetime'])
        response['rows'].append(rows)
    return HttpResponse(json.dumps(response), mimetype='text/json')


def login(request):
    c = RequestContext(request)
    if request.POST:
        try:
            sub = Subscriber.objects.get(login=request.POST['username'])
        except ObjectDoesNotExist:
            return render_to_response("client_login.html", c)
        if sub.password and sub.password == request.POST['password']:
            request.session['subscriber_id'] = sub.id
    elif 'subscriber_id' not in request.session:
        return render_to_response( "client_login.html", c)
    if sub.need_change_password:
        return HttpResponseRedirect("/client/change_password")
    else:
        return HttpResponseRedirect("/client")


def logout(request):
    try:
        del request.session['subscriber_id']
    except KeyError:
        pass
    return HttpResponseRedirect("login")


def osmp_response(response):
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n<response>'
    for k in response:
        xml_str += '\t<{0}>{1}</{0}>\n'.format(k, response[k])
    xml_str += '</response>'
    return HttpResponse(content=xml_str, content_type='text/xml')


def osmp_gate(request):
    osmp_date_format = '%Y%m%d%H%M%S'
    txn_date = datetime.datetime.now()
    ah = None
    response = {'result': 300, 'comment': 'Not enough arguments'}
    error = False
    if not settings.OSMP_ENABLE:
        response.update({'result': 8, 'comment': 'OSMP gate not enable in server config'})
    if {'command', 'txn_id', 'account', 'sum'}.issubset(request.GET.keys()):
        command = request.GET['command']
        try:
            osmp_id = int(request.GET['txn_id'])
        except ValueError:
            error = True
            osmp_id = 0
            response.update({'result': 300, 'comment': 'txn_id ({})not INTEGER'.format(request.GET['txn_id'])})
        response['osmp_txn_id'] = osmp_id
        try:
            value = float(request.GET['sum'])
        except ValueError as e:
            error = True
            value = 0
            response.update({'result': 300, 'comment': 'Can not convert SUM to float'})
        account = request.GET['account']
        try:
            subscriber = Subscriber.objects.get(login__iexact=account, deleted=False)
        except ObjectDoesNotExist as e:
            subscriber = None
            response.update({'result': 5, 'comment': 'Subscriber not found'})
            error = True
        if value < settings.OSMP_MIN_SUM and not error:
            response.update({'result': 241, 'comment': 'SUM too small'})
            error = True
        elif value > settings.OSMP_MAX_SUM and not error:
            response.update({'result': 242, 'comment': 'SUM too big'})
            error = True
        osmp_pay = OsmpPay.objects.filter(osmp_txn_id=osmp_id, command=1, result=0)
        if osmp_pay.count() > 0:
            error = True
            response.update({'result': 300, 'comment': 'Not unique request'})
        if error:
            pass
        elif command == 'check':
            response.update({'result': 0, 'comment': 'OK'})
        elif command == 'pay':
            try:
                txn_date = datetime.datetime.strptime(request.GET['txn_date'], osmp_date_format)
            except Exception as e:
                response.update({'result': 300, 'comment': 'Can not parse txn_date'})
                error = True
            if not error:
                try:
                    ah = AccountHistory(
                        datetime=txn_date,
                        subscriber=subscriber,
                        value=value,
                        owner_type='osm',
                        owner_id=0,
                    )
                    ah.save()
                    response.update({'result': 0, 'comment': 'OK, {}'.format(subscriber.login), 'prv_txn': ah.pk})
                except Exception as error:
                    response.update({'result': 300, 'comment': 'Can not save subscriber'})
                    error = True
        else:
            response.update({'result': 300, 'comment': 'Unknown command'})
            command = 'error'
            error = True
        try:
            command = dict([[f[1],f[0]] for f in OSMP_CHOICES])[command]
        except KeyError:
            command = 666
        osmp_pay = None
        print command
        try:
            osmp_pay = OsmpPay(
                pay_date=txn_date,
                command=command,
                value=value,
                osmp_txn_id=osmp_id,
                prv_txn=ah,
                result=response['result'],
                comment=response['comment'],
                error=error
            )
            osmp_pay.save()
        except:
            if ah:
                if ah.pk:
                    ah.delete()
            response.update({'result': 300, 'comment': 'Unknown command'})
        return osmp_response(response)
    return osmp_response(response)

