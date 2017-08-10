from django.http import HttpResponseRedirect
from vlabs import Config, AppManager
from django.shortcuts import render
from forms import VlabsForm
from pprint import pprint
from env import Var

def index(request):
    getrun = AppManager('test-project')
    name = getrun.getrunning()
    return render(
        request,
        'index.html',
        context={'running_services': name},
    )

def get_name(request):
    pprint(request)
    f = VlabsForm()
    print 'getname  - GET'
            # this is the preferred way to get a users info, it is stored that way
    f.createapp()

    return render(request, 'market.html', {'form': f})

def get_app(request):
    f = VlabsForm()
    print 'getapp'
    pprint(f)
    appradio = request.POST.get('app')
    ri = Config()
    appi = ri.getenv(appradio)
    f.createenv(appi)
    return render(request, 'createapp.html', {'form': f, 'appid':appradio})
def postcreation(request):
    nome = request.POST.dict()
    del nome['csrfmiddlewaretoken']
    e = Var()
    e.buildvar(nome)
    return render(request, 'postcreate.html')
