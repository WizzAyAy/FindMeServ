from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = 'FindMeServ'

urlpatterns = [
    path('server-list/', views.server_list, name='serverList'),
    path('get-players-info/', views.get_players_info, name='getPlayersInfo'),

    path('add-server/', views.add_server, name='addServer'),
    path('add-server-form/', views.add_server, name='addServerForm'),
]

urlpatterns += staticfiles_urlpatterns()
