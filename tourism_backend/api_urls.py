from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Common
    path('user/', include('userapp.api.api_urls')),
    path('ir/', include('indianrailwaysapp.common.api.api_urls')),
    path('pc/', include('productapp.common.api.api_urls')),
    # iDukaan
    path('idukaan/business/', include('businessapp.idukaan.api.api_urls')),
    path('idukaan/ir/', include('indianrailwaysapp.idukaan.api.api_urls')),
    path('idukaan/pc/', include('productapp.idukaan.api.api_urls')),
    # Yatrigan
    path('yatrigan/ir/', include('indianrailwaysapp.yatrigan.api.api_urls')),

    path('mobile/', include('mobileapp.api.api_urls')),
    path('geography/', include('geographyapp.api.api_urls')),
]