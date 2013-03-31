# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from billing.models import *

import datetime
import json
from math import ceil
import time



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
    return render_to_response(template,c)

def only_ip_auth(request,template='client_blocked.html'):
    c = RequestContext(request)
    c['REMOTE_ADDR'] = request.META['REMOTE_ADDR']
    return render_to_response(template,c)

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
    response = {'page':page,'total':total_pages,'records':len(traffic_stat), 'rows':[]}
    for rows in traffic_stat.values()[start:end]:
        rows['datetime'] = str(rows['datetime'])
        response['rows'].append(rows)
    return HttpResponse(json.dumps(response),mimetype='text/json')


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
    return HttpResponseRedirect("/client")


def logout(request):
    try:
        del request.session['subscriber_id']
    except KeyError:
        pass
    return HttpResponseRedirect("login")
