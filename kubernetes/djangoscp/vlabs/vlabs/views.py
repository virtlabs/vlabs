from django.http import HttpResponse
from vlabs import Config
# from vlabs import AppManager
from django.shortcuts import render


def marketplace(request):
    vlcfg = Config()
    # vlam = AppManager()
    cf = vlcfg.getmarket()
    return render(request, 'market.html', {'current_market': cf})



