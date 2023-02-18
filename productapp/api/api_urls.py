from django.urls import path, include

urlpatterns = [
    #PROD
    #DEV
    path('v1/', include('productapp.api.v1.api_urls')),
]