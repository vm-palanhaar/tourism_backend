from django.urls import path, include

urlpatterns = [
    #PROD
    #DEV
    path('v1/', include('indianrailwaysapp.api.v1.api_urls')),
]