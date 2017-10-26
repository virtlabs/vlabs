from django.conf.urls import url
from django.contrib import admin
import views
from views import get_name, get_app, postcreation, to_del, delend

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^marketplace/$', get_name),
    url(r'^running/$', to_del),
    url(r'^app/$', get_app),
    url(r'^postcreate/$', postcreation),
    url(r'^deletion/$', delend),
]