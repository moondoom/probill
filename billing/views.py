# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from billing.models import *
from django.core.exceptions import ObjectDoesNotExist

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
def index(request,template=None):
    c = RequestContext(request)
    if not template:
        template = 'client/main.html'
    return render_to_response(template,c)



def login(request):
    c = RequestContext(request)
    print c
    if request.POST:
        try:
            sub = Subscriber.objects.get(login=request.POST['username'])
        except ObjectDoesNotExist:
            return render_to_response("client/login.html", c)
        if sub.password and sub.password == request.POST['password']:
            request.session['subscriber_id'] = sub.id
    elif 'subscriber_id' not in request.session:
        return render_to_response("client/login.html", c)
    return HttpResponseRedirect("/client")


def logout(request):
    try:
        del request.session['subscriber_id']
    except KeyError:
        pass
    return HttpResponseRedirect("login")
