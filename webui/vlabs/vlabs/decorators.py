from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
import views
from vlabs import Auth



def userisauth(session_func):
    def _wrapped_session_func(request):
        if views.SessionDict.buildSessionDict()[request.session.session_key]:
            return session_func(request)
        else:
            return redirect('index')

    return _wrapped_session_func


def userisadmin(session_admin_func):
    def _wrapped_session_admin_func(request):
        adminauth = views.SessionDict.buildSessionDict()[request.session.session_key]
        if adminauth.users():
            return session_admin_func(request)
        else:
            return HttpResponse(status=403)
    return _wrapped_session_admin_func
