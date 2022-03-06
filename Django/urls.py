from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('FindMeServ.urls')),
    path('', include('Users.urls')),
    path('faceit/', include('Faceit.urls'))
]
