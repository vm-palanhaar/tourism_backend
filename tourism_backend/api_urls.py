from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', admin.site.urls),
    path('yatrigan/', admin.site.urls),
    path('idukaan/', admin.site.urls),
]