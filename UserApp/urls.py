from django.contrib.auth.views import LogoutView
from django.urls import path
from .import views

urlpatterns = [
    path('', views.checkpath),
    path('restrict/', views.restrict, name='restricted'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('otp/', views.OTPVerification.as_view(), name='otpVerification'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
