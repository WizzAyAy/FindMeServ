from django.urls import path

from . import views

app_name = 'FindMeServ'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('add-server/', views.add_server, name='addServer'),
    path('add-server-form/', views.add_server_form, name='addServerForm'),
]
