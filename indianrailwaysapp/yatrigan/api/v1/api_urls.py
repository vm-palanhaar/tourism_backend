from django.urls import path, include

from indianrailwaysapp.yatrigan.api.v1 import api_views as API

urlpatterns = [
    #PROD
    path('trainList', API.TrainListApi.as_view()),
    path('trainSchedule', API.TrainScheduleApi.as_view()),
    path('station/<station>/shop', API.ShopListApi.as_view()),
    path('station/<station>/shop/<shopId>/inv', API.ShopInvListApi.as_view()),
    path('station/<station>/shop/<shopId>', API.ShopInfoApi.as_view()),
    #DEV
]