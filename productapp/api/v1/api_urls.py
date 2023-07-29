from django.urls import path, include

from productapp.api.v1 import api_views as APIv1

urlpatterns = [
    #PROD
    path('product/<str:productId>', APIv1.ProductAPIView.as_view()),
    path('idukaan/', include('productapp.api.v1.idukaan.api_urls')),
    #DEV
]