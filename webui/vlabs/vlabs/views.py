from django.http import HttpResponseRedirect
from vlabs import Config, AppManager
from django.shortcuts import render
from forms import VlabsForm
from pprint import pprint
from env import Var
import re

namespace = 'test-project'

def index(request):
    getrun = AppManager(namespace)
    name = getrun.getrunning()
    rtv2 = []
    timestatus = []
    lab = []
    s = []
    for i in range(0, len(name)):
        timestatus.append(getrun.svcstatus(name[i]))
        lab.append(getrun.getbundle(name[i]))
        s.append(lab[i].split("=")[1])
        print(s)
        rtv2.append(getrun.readroute(getrun.getbundle(name[i])))
    rtv = zip(s, rtv2, timestatus, lab)
    return render(
        request,
        'index.html',
        context={'running_services': rtv}
    )


def get_name(request):
    pprint(request)
    f = VlabsForm()
    print('getname  - GET')
    # this is the preferred way to get a users info, it is stored that way
    f.createapp()

    return render(request, 'market.html', {'form': f})


def get_app(request):
    f = VlabsForm()
    print('getapp')
    pprint(f)
    appradio = request.POST.get('app')
    ri = Config()
    appi = ri.getenv(appradio)
    f.createenv(appi)
    return render(request, 'createapp.html', {'form': f, 'appid': appradio})


def postcreation(request):
    nome = request.POST.dict()
    del nome['csrfmiddlewaretoken']
    e = Var(namespace)
    print(nome)
    e.buildvar(nome)
    return render(request, 'postcreate.html')


def to_del(request):
    getrun = AppManager(namespace)
    name = getrun.getrunning()

    pprint(request)
    f = VlabsForm()
    print('getname  - GET')
    # this is the preferred way to get a users info, it is stored that way
    f.deleteapp()
    return render(request, 'del.html', {'form': f, 'running_services': name})


def delend(request):
    delradio = request.POST.get('run')
    getrun = AppManager(namespace)
    name = getrun.getrunning()
    print("nome dell'applicazione da cancellare" + name[int(delradio)])
    getrun.delete(name[int(delradio)])
    return render(request, 'postdel.html')


def envsvc(request):
    getrun = AppManager(namespace)
    if request.method == 'GET':
        svcsel = request.GET.get('service')
        svc = getrun.listsvc(svcsel)
        serviceenv = getrun.getrunbundleenv(svc)
        return render(request, 'service.html', {'serviceenv': serviceenv, 'bundle': svcsel.split("=")[1], 'service': svcsel})


def delsvc(request):
    getrun = AppManager(namespace)
    dsvc = request.GET.get('service')
    getrun.delete(dsvc)
    return render(request, 'postdel.html')



def test(request):
    getrun2 = AppManager(namespace)
    rtv2 = getrun2.readroute('root1')
    return render(
        request,
        'test.html',
        context={'rtv': rtv2},
    )


