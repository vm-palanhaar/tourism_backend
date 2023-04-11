from django.urls import path, include

from indianrailwaysapp.api.v1.yatrigan import api_views as API

urlpatterns = [
    #PROD
    path('station/<station>/shop/', API.ShopListAPIView.as_view()),
    path('station/<station>/shop/<shopId>/inv/', API.ShopInventoryListAPIView.as_view()),
    path('station/<station>/shop/<shopId>/', API.ShopDetailsAPIView.as_view()),
    #DEV
]