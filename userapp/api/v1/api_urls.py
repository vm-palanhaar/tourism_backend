from django.urls import path

from userapp.api.v1 import api_views as APIv1

urlpatterns = [
    #PROD
    path('register/', APIv1.UserRegisterAPIView.as_view()),
    path('login/', APIv1.UserLoginAPIView.as_view()),
    path('profile/', APIv1.UserProfileAPIView.as_view()),
    #DEV
]