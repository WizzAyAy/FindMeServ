from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import os
import sys
from . import views

sys.path.append(os.path.abspath("views"))

app_name = 'FindMeServ'

urlpatterns = [
    path('server-list/', views.server_list, name='serverList'),
    path('get-players-info/', views.get_players_info, name='getPlayersInfo'),

    # path('add-server/', views.add_server, name='addServer'),
    # path('add-server-form/', views.add_server_form, name='addServerForm'),
]

urlpatterns += staticfiles_urlpatterns()
