from django.urls import path

from . import views

app_name = 'FindMeServ'

urlpatterns = [
    path('test/', views.test, name='test'),
]
