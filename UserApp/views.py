from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from AdminApp.models import *
from StudentApp.urls import *
from TeacherApp.urls import *
from AdminApp.urls import *
from .models import *
from .send_otp import Sent_OTP
from django.views.generic import TemplateView
from django.contrib import messages
from datetime import datetime, timedelta


# Create your views here.


def restrict(request):
    return render(request, 'User/permission.html')


def checkpath(request):
    if request.user.is_authenticated:
        if request.user.role == "principal":
            return redirect('home')
        elif request.user.role == 'student':
            return redirect('SdHome')
        elif request.user.role == 'teacher':
            return redirect('TrHome')
        else:
            return redirect('login')
    else:
        return redirect('login')


class LoginPage(TemplateView):
    template_name = 'Admin/Login_page.html'

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            admin_user = UserProfile.objects.get(username=user)
            Sent_OTP(request, admin_user.email)
            request.session['username'] = username
            return redirect('otpVerification')
        elif user is None:
            if UserProfile.objects.filter(username=username, password=password).exists():
                user = UserProfile.objects.get(username=username, password=password)
                if user is not None:
                    Sent_OTP(request, user.email)
                    request.session['username'] = username
                    return redirect('otpVerification')
                else:
                    pass
            else:
                messages.info(request, 'Username Or Password Is Incorrect...')
                return redirect('login')
        else:
            return redirect('login')


class OTPVerification(TemplateView):
    template_name = 'Admin/OTP_Page.html'

    def post(self, request):
        otp = request.POST['otp']
        username = request.session['username']
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_date = datetime.fromisoformat(otp_valid_date)
            if valid_date > datetime.now():
                if otp_secret_key == otp:
                    user = UserProfile.objects.get(username=username)
                    if user.role == 'student':
                        del request.session['username']
                        del request.session['otp_valid_date']
                        del request.session['otp_secret_key']
                        login(request, user)
                        user.is_updated = datetime.now()
                        user.save()
                        return redirect('SdHome')
                    elif user.role == 'teacher':
                        del request.session['username']
                        del request.session['otp_valid_date']
                        del request.session['otp_secret_key']
                        login(request, user)
                        user.is_updated = datetime.now()
                        user.save()
                        return redirect('TrHome')
                    else:
                        del request.session['username']
                        del request.session['otp_valid_date']
                        del request.session['otp_secret_key']
                        login(request, user)
                        user.is_updated = datetime.now()
                        user.save()
                        return redirect('home')
                else:
                    messages.error(request, 'OTP Is Invalid')
                    return redirect('otpVerification')
            else:
                messages.info(request, 'OTP Has Been Expired')
                return redirect('login')
        else:
            messages.info(
                request, 'Oops Somthing Went Wrong Please Try Again :( ')
            return redirect('login')

