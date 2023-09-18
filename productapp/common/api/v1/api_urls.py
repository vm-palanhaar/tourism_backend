from django.urls import path, include

from productapp.common.api.v1 import api_views as API

urlpatterns = [
    #PROD
    path('prod/<str:productId>', API.ProdInfoApi.as_view()),
    #DEV
]