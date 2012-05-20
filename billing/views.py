from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect


def index(request):
    c = RequestContext(request)
    return render_to_response('client/main.html',c)


def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/client")
        else:
            return HttpResponseRedirect("/client")
    else:
        c = RequestContext(request)
        return render_to_response("templates/main.html", c)


def logout(request):
    c = RequestContext(request)
    return render_to_response('client/main.html',c)
