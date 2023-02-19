from django.urls import path, include

urlpatterns = [
    #PROD
    path('idukaan/', include('organizationapp.api.v1.idukaan.api_urls')),
    #DEV
]