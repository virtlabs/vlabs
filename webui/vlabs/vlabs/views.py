from django.http import HttpResponse, HttpRequest
from vlabs import Config, AppManager, Auth
from django.shortcuts import render, redirect
from forms import VlabsForm
#from pprint import pprint
from env import Var
from decorators import userisauth, userisadmin
from models import ServiceView, UpdateServices
from admin import Adminclass
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

def authnauthz(request):
    user = request.POST.dict()
    username = user['username']
    pwd = user['password']
    if not request.session.session_key:
        request.session.save()
    session = request.session.session_key
    qauth = Auth(session)
    check = qauth.login(username, pwd)
    if check == 0:
        request.session['sessionid'] = request.session.session_key
        request.session['username'] = username
        return redirect("/chns/")
    else:
        return redirect("/")

@userisauth
def chns(request):
    form = False
    qauth = Auth(request.session.session_key)
    prj = qauth.chooseprj()
    if not prj:
        getrun = AppManager(None, request.session.session_key)
        if getrun.users():
            form = VlabsForm()
            form.createns()
        else:
            form = False
    return render(
        request,
        'chns.html', {'initialprj': prj, 'username': request.session['username'], 'form': form})

def cprj(request):
    user = request.POST.dict()
    username = user['username']
    pwd = user['password']
    if not request.session.session_key:
        request.session.save()
    session = request.session.session_key
    qauth = Auth(session)
    check = qauth.login(username, pwd)
    form = False
    if check == 0:
        request.session['sessionid'] = request.session.session_key
        request.session['username'] = username
        prj = qauth.chooseprj()
        if not prj:
            getrun = AppManager(None, request.session.session_key)
            if getrun.users():
                form = VlabsForm()
                form.createns()
            else:
                form = False #####crea pagina di prima creazione namespace, anche sulla stessa pagina. alla classe admin serve solo la sessione dell'admin
        return render(
            request,
            'chns.html', {'initialprj': prj, 'username': username, 'form': form})
    else:
        request.session.flush()
        return redirect('index')

@userisauth
def indexauth(request):
    if request.POST.dict():
        prj = request.POST.dict()
        request.session['project'] = prj
    else:
        prj = request.session['project']
    request.session.save()
    qauth = Auth(request.session.session_key)
    prjtot = qauth.chooseprj()   ###progetti utilizzabili dall'utente

    ##Appmanager
    SessionDict.buildSessionDict()[request.session.session_key] = AppManager(prj['prj'], request.session.session_key)
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    dictbundle = {}
    ###running svcs, 'bundle' ->label
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
    if getrun.users():
        admbtt = 1
    else:
        admbtt = 0
    return render(
        request,
        'indexsvc.html',
        context={'dictbundle': dictbundle, 'donutdict': donutdict, 'prj': prjtot, 'admbtt': admbtt, 'actualprj': prj['prj']}
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
        return HttpResponse(content=json.dumps(donutupdate))
    else:
        logging.warning ("request not ajax - ERROR")


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
    donutuser = []
    adminclass = Adminclass(request.session.session_key)
    nodescheck = adminclass.listnodes()
    for j in dictnsusr:
        donutuser.append({
            'label' : j,
            'value': len(dictnsusr[j]['Users'])
        })
    return render(
        request,
        'adminsvcs.html',
        context={'activesvcs': activesvcs, 'usrschart': usrschart, 'prj': prj, 'donutuser': donutuser, 'dictnsusr': dictnsusr, 'nodescheck': nodescheck})


@userisauth
@userisadmin
def funcns(request):
    if request.GET.get('namespace'):
        namespace = request.GET.get('namespace')
        request.session['project']['prj'] = namespace
        request.session.save()
    else:
        namespace = request.session['project']['prj']
    adminclass = Adminclass(request.session.session_key)
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    serviceview = ServiceView()
    #ns list
    qauth = Auth(request.session.session_key)
    prj = qauth.chooseprj()
    users = getrun.users('list')
    nsusers = serviceview.usersperns(getrun.rolebinding(namespace)) ####namespaced user
    #users list
    usrschart = serviceview.userschart(users)
    nssvcs = adminclass.readnsdc(namespace)
    #pprint(nssvcs) ###last status Check!
    quotas = adminclass.readquotas(namespace).items
    lmts = adminclass.readlimits(namespace)
    limits = serviceview.limitsformat(lmts)
    nodescheck = adminclass.listnodes()
    fql = VlabsForm()
    fql.setlimits(namespace)
    return render(
        request,
        'namespace.html',
        context={'namespace': namespace, 'prj': prj, 'nodescheck': nodescheck ,'usrschart': usrschart, 'nssvcs': nssvcs, 'quotas': quotas, 'limits': limits, 'formlim':fql, 'nsusers': nsusers})


@userisauth
@userisadmin
def limquot(request):
    namespace = request.POST.get('namespace')
    adminclass = Adminclass(request.session.session_key)
    tl = adminclass.readalllimits()
    allquotas = adminclass.readallquotas()
    return render(
        request,
        'tuneup.html', context={'namespace': namespace, 'totallimits': tl, 'quotas': allquotas})

@userisauth
@userisadmin
def dellimq(request):
    if request.GET:
        var = request.GET.dict()
        namespace = request.session['project']['prj']
        adminclass = Adminclass(request.session.session_key)
        if 'limit' in var:
            adminclass.dellimit(var['limit'], namespace)
        if 'quota' in var:
            adminclass.delquota(var['quota'], namespace)
    return redirect("/namespace/", namespace)

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
        adminclass.setlimits(var['newnamespace'], newlim)
    if 'quota' in var:
        oldquota = adminclass.readsinglequota(var['ns'], var['quota'])
        newquota = {'metadata': {'name': var['quota'], 'labels': {'label':'vlabs'}}}
        newquota['spec'] = {}
        newquota['spec'] = oldquota.spec
        adminclass.setquotas(var['newnamespace'], newquota)

    return render(
        request,
        'test.html',
        context={'var': var},
    )


@userisauth
@userisadmin
def funcuser(request):
    if request.GET:
        user = request.GET.get('user')
        request.session['project']['user'] = user
        request.session.save()
    else:
        user = request.session['project']['user']
    #std objects
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    qauth = Auth(request.session.session_key)
    serviceview = ServiceView()
    adminclass = Adminclass(request.session.session_key)
    ##### end std object
    userdict = adminclass.readuser(user)
    #adminpage-xtendedtemplate
    prj = qauth.chooseprj()
    users = getrun.users('list')
    usrschart = serviceview.userschart(users)
    nodescheck = adminclass.listnodes()
    ##### end end xtendedtemplate
    dictprj = {}
    dictnsusr = {}
    newprj = prj
    for i in prj:
        dictnsusr[i] = {}
        dictnsusr[i]['Users'] = serviceview.usersperns(getrun.rolebinding(i))
    nsperuser = serviceview.nsperuser(user, dictnsusr)
    for key in nsperuser[user]:
        nsperuser[user][key] = getrun.getrunningadmin(key)
        newprj.remove(key)
    return render(
        request,
        'user.html',
        context={'user': user, 'prj': prj, 'usrschart': usrschart, 'nodescheck': nodescheck, 'userdict': userdict, 'nsperuser':nsperuser[user], 'newprj':newprj})

@userisauth
@userisadmin
def patchrolebindings(request):
    newrole = request.POST.dict()
    adminclass = Adminclass(request.session.session_key)
    adminclass.replacerolebinding(newrole['namespace'], newrole['user'], newrole['operation'])
    return redirect("/user/")

@userisauth
@userisadmin
def newns(request):
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    qauth = Auth(request.session.session_key)
    serviceview = ServiceView()
    adminclass = Adminclass(request.session.session_key)
    ##### end std object
    # adminpage-xtendedtemplate
    prj = qauth.chooseprj()
    users = getrun.users('list')
    usrschart = serviceview.userschart(users)
    nodescheck = adminclass.listnodes()
    ##### end end xtendedtemplate
    form = VlabsForm()
    form.createns()
    return render(
        request,
        'newns.html',
        context={'prj': prj, 'usrschart': usrschart, 'nodescheck': nodescheck, 'form': form})

@userisauth
def nscreated(request):
    adminclass = Adminclass(request.session.session_key)
    if request.POST:
        dict = request.POST.dict()
        newns = dict['namespacename']
        if adminclass.createns(newns, request.session['username']):
            if 'first' in dict:
                return redirect("/chns/")
            else:
                return redirect("/adminsvcs/")
        else:
            return redirect("/newns/")

@userisauth
def newtab(request):
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    name = getrun.getrunning('bundle')

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
    f = VlabsForm()
    f.createapp()

    return render(request, 'market.html', {'form': f})

@userisauth
def get_app(request):
    f = VlabsForm()
    appradio = request.POST.get('app')
    ri = Config()
    appi = ri.getenv(appradio)
    f.createenv(appi)
    return render(request, 'createapp.html', {'form': f, 'appid': appradio, 'appi': appi})

@userisauth
def postcreation(request):
    nome = request.POST.dict()
    del nome['csrfmiddlewaretoken']
    prj = request.session['project']['prj']
    user = request.session.get('sessionid')
    e = Var(prj, user)
    e.buildvar(nome)
    return render(request, 'postcreate.html')


@userisauth
def delend(request):
    delradio = request.POST.get('run')
    getrun = SessionDict.buildSessionDict()[request.session.session_key]
    name = getrun.getrunning()
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
    return redirect("/")

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
    return redirect("/indexsvc/")

@userisadmin
@userisauth
def updaterc(request):
    var = request.POST.dict()
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
