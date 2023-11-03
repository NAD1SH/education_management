from django.contrib.auth.decorators import user_passes_test
from UserApp.urls import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user

def is_teacher(request):
    if request.user.is_authenticated and request.user.role == "teacher" :
        return True
    elif request.user.is_anonymous:
        return "anonymous"
    elif request.user.role != "teacher":
        return False

class TeacherRequiredMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        def check_teacher(request, *args, **kwargs):
            return_check = is_teacher(request)
            if return_check == True:
                return view(request, *args, **kwargs)
            elif return_check == "anonymous":
                return HttpResponseRedirect(reverse('login'))
            else:
                return HttpResponseRedirect(reverse('restricted'))   
        return check_teacher


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