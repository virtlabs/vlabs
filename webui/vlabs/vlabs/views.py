from django.http import HttpResponse, HttpRequest
from vlabs import Config, AppManager, Auth
from django.shortcuts import render, redirect
from forms import VlabsForm
from pprint import pprint
from env import Var
from decorators import userisauth, userisadmin
from models import ServiceView, UpdateServices
from admin import Adminclass
import ast
from django.core import serializers
import re
import tempfile
from collections import MutableMapping
import json

class SessionDict:
    ssd = {}

    @staticmethod
    def buildSessionDict():
        if SessionDict.ssd == None:
            SessionDict.ssd = {}
        return SessionDict.ssd

def index(request):
    f = VlabsForm()
    f.auth()
    return render(
        request,
        'index.html', {'form': f})

def cprj(request):
    user = request.POST.dict()
    username = user['username']
    pwd = user['password']
    if not request.session.session_key:
        request.session.save()
    session = request.session.session_key
    print("CONTROLLO SESSION IN VIEW - INIZIO \n \n" + str(session) + "\n \n CONTROLLO SESSION IN VIEW - FINE")
    qauth = Auth(session)
    check = qauth.login(username, pwd)
    if check == 0:
        request.session['sessionid'] = request.session.session_key
        request.session['username'] = username
        prj = qauth.chooseprj()
        return render(
            request,
            'chns.html', {'initialprj': prj, 'username': username})
    else:
        request.session.flush()
        return redirect('index')


def indexauth(request):
    if request.POST.dict():
        prj = request.POST.dict()
        request.session['project'] = prj
        print("INDEXAUTH")
        print(request.session['project'])
    else:
        prj = request.session['project']
        print("INDEXAUTH-ELSE")
        print(prj)
    request.session.save()
    qauth = Auth(request.session.session_key)
    prjtot = qauth.chooseprj()   ###progetti utilizzabili dall'utente

    ##instanzio Appmanager
    SessionDict.buildSessionDict()[request.session.session_key] = AppManager(prj['prj'], request.session.session_key)
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    #request.session['prj'] =  prj['prj']
    dictbundle = {}
    ###running svcs con 'bundle' nelle label
    name = getrun.getrunning('bundle')
    for k in name.keys():
        dictbundle[k] = {}
        for x in range(0, len(name[k])):
            dictbundle[k][name[k][x]] = {}
            dictbundle[k][name[k][x]]['bundlename'] = getrun.getbundle(name[k][x])
            dictbundle[k][name[k][x]]['timestamp'] = getrun.svctime(name[k][x])
            dictbundle[k][name[k][x]]['status'] = getrun.svcstatus(name[k][x])
            dictbundle[k][name[k][x]]['route'] = getrun.readroute(dictbundle[k][name[k][x]]['bundlename'])
    serviceview = ServiceView()
    donutdict = serviceview.dchart(dictbundle)
    #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nDICTBUNDLE")
    #print(dictbundle)
    #print("\n\n\n\n\n\nDONUTDICT")
    #print(donutdict)
    if getrun.users():
        admbtt = 1
    else:
        admbtt = 0
    return render(
        request,
        'indexsvc.html',
        context={'dictbundle': dictbundle, 'donutdict': donutdict, 'prj': prjtot, 'admbtt': admbtt}
    )


@userisauth
def svcupdate(request):
    if request.is_ajax():
        getrun = SessionDict.buildSessionDict()[request.session.session_key]
        dictbundle = {}
        name = getrun.getrunning('bundle')
        for k in name.keys():
            dictbundle[k] = {}
            for x in range(0, len(name[k])):
                dictbundle[k][name[k][x]] = {}
                dictbundle[k][name[k][x]]['bundlename'] = getrun.getbundle(name[k][x])
                dictbundle[k][name[k][x]]['timestamp'] = getrun.svctime(name[k][x])
                dictbundle[k][name[k][x]]['status'] = getrun.svcstatus(name[k][x])
                dictbundle[k][name[k][x]]['route'] = getrun.readroute(dictbundle[k][name[k][x]]['bundlename'])
        serviceview = ServiceView()
        donutupdate = serviceview.dchart(dictbundle)
        #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nDICTBUNDLE")
        #print(dictbundle)
        #print("\n\n\n\n\n\nDONUTDICT")
        #print(donutupdate)
        return HttpResponse(content=json.dumps(donutupdate))
    else:
        print ("ERROR")


@userisauth
@userisadmin
def adminsvcs(request):
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    qauth = Auth(request.session.session_key)
    prj = qauth.chooseprj()
    serviceview = ServiceView()
    dictprj = {}
    dictnsusr = {}
    for i in prj:
        dictnsusr[i] = {}
        dictprj[i] = getrun.getrunningadmin(i)
        dictnsusr[i]['Users'] = serviceview.usersperns(getrun.rolebinding(i))
        dictnsusr[i]['Volumes'] = serviceview.pvpvcs(getrun.getpvpvcs(i))
    activesvcs = serviceview.adminbarchart(dictprj)
    users = getrun.users('list')
    usrschart = serviceview.userschart(users)
    #print(dictnsusr) ###dictnsusr = dizionario con namespaces e utenti associati e pv/pvc
    donutuser = []
    for j in dictnsusr:
        donutuser.append({
            'label' : j,
            'value': len(dictnsusr[j]['Users'])
        })
    return render(
        request,
        'adminsvcs.html',
        context={'activesvcs': activesvcs, 'usrschart': usrschart, 'prj': prj, 'donutuser': donutuser, 'dictnsusr': dictnsusr})


@userisauth
@userisadmin
def funcns(request):
    namespace = request.GET.get('namespace')
    adminclass = Adminclass(request.session.session_key)
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    serviceview = ServiceView()
    #ns list
    qauth = Auth(request.session.session_key)
    prj = qauth.chooseprj()
    users = getrun.users('list')
    #users list
    usrschart = serviceview.userschart(users)
    nssvcs = adminclass.readnsdc(namespace)
    pprint(nssvcs) ###last status Check!
    quotas = adminclass.readquotas(namespace).items
    lmts = adminclass.readlimits(namespace)
    limits = serviceview.limitsformat(lmts)
    fql = VlabsForm()
    fql.setlimits(namespace)
    # replication controller
    # replication controller
    return render(
        request,
        'namespace.html',
        context={'namespace': namespace, 'prj': prj, 'usrschart': usrschart, 'nssvcs': nssvcs, 'quotas': quotas, 'limits': limits, 'formlim':fql})


@userisauth
@userisadmin
def limquot(request):
    namespace = request.POST.get('namespace')
    adminclass = Adminclass(request.session.session_key)
    serviceview = ServiceView()
    forms = VlabsForm()
    #Limits
    actuallimits = adminclass.readlimits(namespace)
    tl = adminclass.readalllimits()
    allquotas = adminclass.readallquotas()
    return render(
        request,
        'tuneup.html', context={'namespace': namespace, 'totallimits': tl, 'quotas': allquotas})

@userisauth
@userisadmin
def setql(request):
    adminclass = Adminclass(request.session.session_key)
    if request.POST:
        var = request.POST.dict()
    if 'limit' in var:
        oldlim = adminclass.readlimit(var['ns'], var['limit'])
        newlim = {'metadata': {'name': var['limit'], 'labels': {'label':'vlabs'}}}
        newlim['spec'] = {}
        newlim['spec'] = oldlim.spec
        print(newlim)
        adminclass.setlimits(var['newnamespace'], newlim)
    if 'quota' in var:
        oldquota = adminclass.readsinglequota(var['ns'], var['quota'])
        print(oldquota)
        newquota = {'metadata': {'name': var['quota'], 'labels': {'label':'vlabs'}}}
        newquota['spec'] = {}
        newquota['spec'] = oldquota.spec
        print(newquota)
        adminclass.setquotas(var['newnamespace'], newquota)

    return render(
        request,
        'test.html',
        context={'var': var},
    )


@userisauth
@userisadmin
def funcuser(request):
    user = request.GET.get('user')
    print(user)
    return render(
        request,
        'user.html',
        context={'user': user})


@userisauth
def newtab(request):
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    name = getrun.getrunning('bundle') # QUI ARGS

    dictbundle = {}

    for k in name.keys():
        dictbundle[k] = {}
        for x in range(0, len(name[k])):
            dictbundle[k][name[k][x]] = {}
            dictbundle[k][name[k][x]]['bundlename'] = getrun.getbundle(name[k][x])
            dictbundle[k][name[k][x]]['timestamp'] = getrun.svctime(name[k][x])
            dictbundle[k][name[k][x]]['status'] = getrun.svcstatus(name[k][x])
            dictbundle[k][name[k][x]]['route'] = getrun.readroute(dictbundle[k][name[k][x]]['bundlename'])
    serviceview = ServiceView()
    donutdict = serviceview.dchart(dictbundle)
    return render(request, 'newtab.html', {'dictbundle': dictbundle, 'donutdict': donutdict})

@userisauth
def get_name(request):
    pprint(request)
    f = VlabsForm()
    print('getname  - GET')
    # this is the preferred way to get a users info, it is stored that way
    f.createapp()

    return render(request, 'market.html', {'form': f})

@userisauth
def get_app(request):
    f = VlabsForm()
    print('getapp')
    pprint(f)
    appradio = request.POST.get('app')
    ri = Config()
    appi = ri.getenv(appradio)
    f.createenv(appi)
    return render(request, 'createapp.html', {'form': f, 'appid': appradio, 'appi': appi})

@userisauth
def postcreation(request):
    nome = request.POST.dict()
    print("NOMEEEEEEEEEEEEEEEEEEEEEEE")
    print(nome)
    print("NOMEEEEEEEEEEEEEEEEEEEEEEE")
    del nome['csrfmiddlewaretoken']
    prj = request.session['project']['prj']
    user = request.session.get('sessionid')
    e = Var(prj, user)
    e.buildvar(nome)
    return render(request, 'postcreate.html')

'''
def to_del(request):
    getrun = AppManager(namespace)
    name = getrun.getrunning()

    pprint(request)
    f = VlabsForm()
    print('getname  - GET')
    # this is the preferred way to get a users info, it is stored that way
    f.deleteapp()
    return render(request, 'del.html', {'form': f, 'running_services': name})
'''

@userisauth
def delend(request):
    delradio = request.POST.get('run')
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    name = getrun.getrunning()
    print("nome dell'applicazione da cancellare" + name[int(delradio)])
    getrun.delete(name[int(delradio)])
    return render(request, 'postdel.html')

@userisauth
def envsvc(request):
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    qauth = Auth(request.session.session_key)
    prjtot = qauth.chooseprj()  ###progetti utilizzabili dall'utente
    if getrun.users():
        admbtt = 1
    else:
        admbtt = 0
    if request.method == 'GET':
        svcsel = request.GET.get('service')
        svc = getrun.listsvc(svcsel)
        serviceenv = getrun.getrunbundleenv(svc)
        f = VlabsForm()
        f.chooseapp(svcsel)
        print("SVCSEL")
        print(svcsel)
        print("SVCSEL")
        return render(request, 'service.html', {'serviceenv': serviceenv, 'bundle': svcsel.split("=")[1], 'service': svcsel, 'prj': prjtot, 'admbtt': admbtt, 'form': f})

@userisauth
def delsvc(request):
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    dsvc = request.GET.get('service')
    getrun.delete(dsvc)
    return render(request, 'postdel.html')

@userisauth
def logout(request):
    rmauthz = Auth(request.session.session_key)
    rmauthz.logout()
    request.session.flush()
    SessionDict.ssd = {}
    return render(request, 'logout.html')

@userisauth
def updatevar(request):
    app = request.POST.get('app')
    service = request.POST.get('service')
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    svc = getrun.listsvc(app)
    serviceenv = getrun.getrunbundleenv(svc)
    f = VlabsForm()
    f.updatevariables(serviceenv[service])
    del serviceenv[service]
    return render(request, 'update.html', {'app':serviceenv, 'f': f, 'service': service})

@userisauth
def updatedvar(request):
    newvars = request.POST.dict()
    service = newvars['service']
    del newvars['csrfmiddlewaretoken']
    uptd = UpdateServices()
    data = uptd.varupdate(newvars)
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    getrun.patchdcvar(service, request.session['project']['prj'], data)
    return render(request, 'updatedvar.html')

@userisadmin
@userisauth
def updaterc(request):
    var = request.POST.dict()
    print(var)
    adminclass = Adminclass(request.session.session_key)
    body = {'spec': {'replicas': int(var['quantity'])}}
    adminclass.updatedconfig(var['name'], var['namespace'], body)
    return render(
        request,
        'test.html',
        context={'var': var},
    )

def test(request):
    var = request.POST.dict()
    return render(
        request,
        'test.html',
        context={'var': var},
    )
            
