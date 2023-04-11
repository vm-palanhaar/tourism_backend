from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('ir/', include('indianrailwaysapp.api.api_urls')),
    path('user/', include('userapp.api.api_urls')),
    path('pc/', include('productapp.api.api_urls')),
    path('business/', include('businessapp.api.api_urls')),
    path('mobile/', include('mobileapp.api.api_urls')),
    path('geography/', include('geographyapp.api.api_urls')),
]