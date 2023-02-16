from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('ir/', include('indianrailwaysapp.api.api_urls')),
    path('user/', include('userapp.api.api_urls')),
    path('yatrigan/', admin.site.urls),
    path('idukaan/', admin.site.urls),
]