from django.contrib.auth.decorators import user_passes_test
from UserApp.urls import *
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import get_user

def is_admin(request):
    if request.user.is_authenticated and request.user.role == "principal" :
        return True
    elif request.user.is_anonymous:
        return "anonymous"
    elif request.user.role != "principal":
        return False

class AdminRequiredMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        def check_admin(request, *args, **kwargs):
            return_check = is_admin(request)
            if return_check == True:
                return view(request, *args, **kwargs)
            elif return_check == "anonymous":
                return HttpResponseRedirect(reverse('login'))
            else:
                return HttpResponseRedirect(reverse('restricted')) 
        return check_admin


def admin_required(view_func):
    def check_admin(request, *arg, **kwargs):
        anonymous = get_user(request)
        if anonymous.is_anonymous:
            return redirect('login')
        else:
            if request.user.role == "principal" and request.user.is_authenticated:
                return view_func(request, *arg, **kwargs)
            else:
                return redirect('restricted')
    return check_admin


def is_Authenticated(request):
    return request.user.is_authenticated

class LoginRequiredMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        def check_authenticated(request, *args, **kwargs):
            if is_Authenticated(request):
                return view(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('login'))
        return check_authenticated