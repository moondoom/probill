# -*- coding: utf-8 -*-
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from models import MenuItems
from django.contrib.auth.views import login_required
from django.db.models import Q


@login_required()
def index(request):
    context = RequestContext(request)
    context['menu_items'] =  MenuItems.tree.all()
    context['menu_items'] = context['menu_items'].filter(Q(view_perm__in=request.user.get_all_permissions())|\
                                                         Q(view_perm=None))
    for x in context['menu_items']:
        print x
    print request.user.get_all_permissions()
    return render_to_response('moon/admin.html',context)

def login(request):
    from django.contrib.auth.views import login
    return login(request)