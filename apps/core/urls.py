from django.urls import path
from django.shortcuts import redirect
from . import views


def redirect_to_docs(request):
    return redirect('schema-swagger-ui')


urlpatterns = [
    path('', redirect_to_docs, name='root'),
    path('health/', views.health_check, name='health-check'),
]
