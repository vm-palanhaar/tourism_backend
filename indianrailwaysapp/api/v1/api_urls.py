from django.urls import path, include

from indianrailwaysapp.api.v1 import api_views as API


urlpatterns = [
    #PROD
    path('station', API.RailStationListApi.as_view()),
    path('helpline', API.IrHelplineListApi.as_view()),
    path('helpline/grp', API.IrGRPListApi.as_view()),
    path('idukaan/', include('indianrailwaysapp.api.v1.idukaan.api_urls')),
    path('yatrigan/', include('indianrailwaysapp.api.v1.yatrigan.api_urls')),
    #DEV
]