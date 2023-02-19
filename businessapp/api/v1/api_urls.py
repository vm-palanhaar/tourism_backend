from django.urls import path, include

urlpatterns = [
    #PROD
    path('idukaan/', include('businessapp.api.v1.idukaan.api_urls')),
    #DEV
]