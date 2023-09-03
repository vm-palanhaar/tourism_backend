from django.urls import path, include

from indianrailwaysapp.common.api.v1 import api_views as API


urlpatterns = [
    #PROD
    path('stations', API.RailStationListApi.as_view()),
    path('helplines', API.IrHelplineListApi.as_view()),
    path('helplines/grp', API.IrGRPListApi.as_view()),
    #DEV
]