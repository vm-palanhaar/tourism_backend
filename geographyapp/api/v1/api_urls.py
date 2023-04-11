from django.urls import path, include

from geographyapp.api.v1 import api_views as API

urlpatterns = [
    #PROD
    path('<str:cid>/states/', API.StateAPIView.as_view()),
    #DEV
    #path('rev-geo/', API.ReverseGeocodeAPIView.as_view()),

]