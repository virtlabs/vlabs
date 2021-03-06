from django.conf.urls import url
from django.contrib import admin
import views
from views import adminsvcs, get_name, get_app, postcreation, delend, test, envsvc, dellimq, delsvc, setql, newtab, indexauth, chns, logout, svcupdate, funcns, funcuser, updaterc, updatevar, updatedvar, limquot, patchrolebindings, newns, nscreated, authnauthz
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^auth/', authnauthz),
    url(r'^indexsvc/', indexauth),
    url(r'^admin/', admin.site.urls),
    url(r'^marketplace/$', get_name),
    url(r'^chns/$', chns),
    url(r'^app/$', get_app),
    url(r'^postcreate/$', postcreation),
    url(r'^deletion/$', delend),
    url(r'^del/$', delsvc),
    url(r'^service/$', envsvc),
    url(r'^logout/$', logout),
    url(r'^test/$', test),
    url(r'^svcupdate/$', svcupdate, name='svcupdate'),
    url(r'^namespace/$', funcns),
    url(r'^user/$', funcuser),
    url(r'^adminsvcs/$', adminsvcs),
    url(r'^update/$', updatevar),
    url(r'^updatedvar/$', updatedvar),
    url(r'^limitsandquotas/$', limquot),
    url(r'^setql/$', setql),
    url(r'^updaterc/$', updaterc),
    url(r'^dellimq/$', dellimq),
    url(r'^patchrolebindings/$', patchrolebindings),
    url(r'^newns/$', newns),
    url(r'^nscreated/$', nscreated),


]