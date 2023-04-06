from django.urls import path, include

from indianrailwaysapp.api.v1 import api_views as APIv1

urlpatterns = [
    #PROD
    path('station/', APIv1.RailwayStationListAPIView.as_view()),
    path('grp/', APIv1.IrGRPListAPIView.as_view()),
    path('grp/rev-geo', APIv1.IrGRPStateAPIView.as_view()),
    path('idukaan/', include('indianrailwaysapp.api.v1.idukaan.api_urls')),
    path('yatrigan/', include('indianrailwaysapp.api.v1.yatrigan.api_urls')),
    #DEV
]