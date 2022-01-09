from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'FindMeServ'

urlpatterns = [
    path('', views.home, name='home'),
    # path('server-list/', views.server_list, name='serverList'),
    path('add-server/', views.add_server, name='addServer'),
    # path('add-server-form/', views.add_server_form, name='addServerForm'),
    path('get-players-info/', views.get_players_info, name='getPlayersInfo'),
]

urlpatterns += staticfiles_urlpatterns()
