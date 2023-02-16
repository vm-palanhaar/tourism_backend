from django.urls import path

from indianrailwaysapp.api.v1 import api_views as APIv1

urlpatterns = [
    #PROD
    path('station/', APIv1.RailwayStationListAPIView.as_view()),
    #DEV
]