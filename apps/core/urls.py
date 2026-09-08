from django.urls import path
from django.shortcuts import redirect
from . import views


def redirect_to_login(request):
    return redirect('/login.html')


urlpatterns = [
    path('', redirect_to_login, name='root'),
    path('health/', views.health_check, name='health-check'),
]
