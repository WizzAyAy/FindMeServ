from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = 'Faceit'

urlpatterns = [
    path('get-room/', views.get_room, name='getRoom'),
    path('get-room-stats/', views.get_room_stats, name='getRoomStats'),
]

urlpatterns += staticfiles_urlpatterns()